# from django.shortcuts import render
import os
import uuid
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin  # 上位に記載必要
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, get_user_model
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.shortcuts import render, redirect

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.http import HttpResponseRedirect
# from django.http import Http404

from .models import Item, ItemPhoto

# from django.forms.models import model_to_dict  # debug用に追加
from .forms import (
    CustomUserCreationForm,
    LoginForm,
    ItemCreateForm,
    PhotoUploadForm,
)

User = get_user_model()


# Create your views here.
# ユーザー新規登録
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


# ユーザーログイン
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

    # ログイン状態の保持
    # form.pyにてバリデーション成功すると以下処理が実行される
    def form_valid(self, form):
        user = form.get_user()  # 認証に成功したuserインスタンス
        login(
            self.request, user
        )  # 認証済みユーザーをセッションに登録し、以降のリクエストでログイン状態を維持する
        user.last_login = now()
        user.save()
        return super().form_valid(form)  # 標準のリダイレクト処理などを実行

    def get_success_url(self):
        return reverse_lazy("item-list")


# アイテム一覧表示
class ItemListView(LoginRequiredMixin, ListView):
    template_name = "items/index.html"
    context_object_name = "items"  # テンプレートにて使用する変数名

    # 一覧表示に必要な情報（モデルから取り出したデータの集まり）を定義。
    def get_queryset(self):
        user = self.request.user  # ログインしているユーザー情報を取得

        return Item.objects.filter(
            user=user, delete_flag=False
        )  # ユーザーに紐づく、論理削除されていないアイテムを取得


# アイテム新規登録
class ItemCreateView(LoginRequiredMixin, View):
    # 許可するHTTPメソッドを制限（GETとPOSTのみ）
    http_method_names = ["get", "post"]
    template_name = "items/create.html"

    # GETリクエスト（フォーム表示）
    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "form": ItemCreateForm(),  # アイテム登録フォーム
                "photo_form": PhotoUploadForm(),  # 画像アップロードフォーム
            },
        )

    # POSTリクエスト（登録処理）
    def post(self, request, *args, **kwargs):
        # 送信データをフォームにバインド
        form = ItemCreateForm(request.POST)
        photo_form = PhotoUploadForm(request.POST, request.FILES)

        # フォームが無効な場合はエラーを表示して再描画
        if not form.is_valid() or not photo_form.is_valid():
            messages.error(
                request,
                f"ItemCreateForm: {form.errors} / PhotoForm: {photo_form.errors}",
            )
            return render(
                request, self.template_name, {"form": form, "photo_form": photo_form}
            )

        # Itemモデルを保存（ユーザーとシーズンを設定）
        item = form.save(commit=False)

        item.user = request.user

        # (TODO)seasonは暫定で以下のように設定
        item.season = 0
        item.save()

        # M2M があればここで
        form.save_m2m()

        # 複数画像保存 → URL 取得
        for img in request.FILES.getlist("images"):
            # 拡張子を推定（なければ jpg など固定でもOK）

            ext = os.path.splitext(img.name)[1] or ".jpg"

            filename = f"items/{uuid.uuid4()}{ext}"

            # ストレージに保存
            saved_path = default_storage.save(filename, ContentFile(img.read()))

            # 公開URL（S3 等なら presigned の代わりに storage.url を使う想定）
            public_url = default_storage.url(saved_path)

            # ★フィールド名をモデルに合わせる（例：url）
            ItemPhoto.objects.create(item=item, url=public_url)

        # 一覧ページへリダイレクト
        return redirect("item-list")


# アイテム詳細
class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "items/detail.html"
    context_object_name = "item"

    # Itemクラスの中のログインしているユーザーの商品を取得
    def get_queryset(self):
        user = self.request.user

        return Item.objects.filter(
            user=user, delete_flag=False
        )  # 削除されていないアイテム


# アイテム削除機能
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    context_object_name = "item"  # テンプレートにて使用する変数名
    success_url = reverse_lazy("item-list")  # 削除後のリダイレクト先

    # Itemモデルより削除アイテムのデータを取得し、delete_flagをTrueへ変更し保存
    # 論理削除のため親クラスを呼び出さず、postメソッドをオーバーライドする
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # URLより削除対象の1つのデータを取得

        # 削除済フラグをTrueにて保存
        self.object.delete_flag = True
        self.object.save()

        # ItemPhotoモデルの情報もdelete_flagをTrueへ変更し保存
        for photo in self.object.itemphoto_set.all():  # 削除対象のアイテムに紐づく写真（itemphoto_set)をすべて取り出し順番に処理する
            photo.delete_flag = True
            photo.save()

        # Trueへ変更後、success_urlへリダイレクトする
        return HttpResponseRedirect(self.get_success_url())
