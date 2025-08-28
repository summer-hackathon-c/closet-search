import os
import uuid
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin  # 上位に記載必要
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, get_user_model
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.shortcuts import render, redirect

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.http import HttpResponseRedirect

# from django.http import Http404
from .models import Item, ItemPhoto
from .forms import (
    CustomUserCreationForm,
    LoginForm,
    ItemCreateForm,
    ItemUpdateForm,
    SeasonsSelectForm,
)

# from django.forms.models import model_to_dict
from django.db.models import OuterRef, Subquery

User = get_user_model()


# Create your views here.
# ユーザー新規登録
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "登録しました！ログインしてください。")
        return response


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


# ログイン状態を判定してリダイレクトするビューを設定するクラス
class RootRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ログイン時は一覧ページへ
            return redirect("item-list")
        else:
            # 未ログイン時はログインページへ
            return redirect("login")


# アイテム一覧表示
class ItemListView(LoginRequiredMixin, ListView):
    template_name = "items/index.html"
    context_object_name = "items"  # テンプレートにて使用する変数名

    # 一覧表示に必要な情報（モデルから取り出したデータの集まり）を定義。
    def get_queryset(self):
        user = self.request.user  # ログインしているユーザー情報を取得

        first_photo = (
            ItemPhoto.objects.filter(item=OuterRef("pk"))
            .order_by("id")
            .values("url")[:1]
        )

        return (
            Item.objects.filter(user=user, delete_flag=False)
            .annotate(first_photo_url=Subquery(first_photo))
            .order_by("-purchase_date", "-id")
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
                "season_form": SeasonsSelectForm(),  # 季節タグ登録フォーム
            },
        )

    # POSTリクエスト（登録処理）
    def post(self, request, *args, **kwargs):
        # 送信データをフォームにバインド
        form = ItemCreateForm(request.POST, request.FILES)
        season_form = SeasonsSelectForm(request.POST)

        # imagesの枚数チェック
        images = request.FILES.getlist("images")
        item_valid = form.is_valid()
        if len(images) < 1:
            form.add_error("images", "写真は最低１枚登録してください")
        elif len(images) > 5:
            form.add_error("images", "写真は最大５枚まで登録できます")

        season_valid = season_form.is_valid()

        # どちらかNGなら、両方のエラーを持ったまま再描画
        if not (item_valid and season_valid) or form.errors or season_form.errors:
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "season_form": season_form,
                },
            )

        # ここから保存処理
        item = form.save(commit=False)
        item.user = request.user
        item.season = season_form.get_season_value()
        item.delete_flag = False
        item.save()

        # 複数画像保存 → URL 取得
        for img in images:
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

    # テンプレートへ渡す表示用データ（コンテキスト）をカスタマイズ。
    # get_context_dataをオーバーライドしている。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        labels = [
            label
            for value, label in SeasonsSelectForm.SEASON_FLAGS
            if item.season & value
        ]
        context["season_labels"] = labels
        return context


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

        # Trueへ変更後、success_urlへリダイレクトする
        return HttpResponseRedirect(self.get_success_url())


# アイテム編集
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = "items/edit.html"
    form_class = ItemUpdateForm
    context_object_name = "item"

    # テンプレートへデータを定義（オーバーライド）
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # すでに保存されているアイテムの季節情報（整数）をもとに、チェックボックスの初期状態を決定
        season_initial = {
            "spring": bool(self.object.season & SeasonsSelectForm.SEASON_SPRING),
            "summer": bool(self.object.season & SeasonsSelectForm.SEASON_SUMMER),
            "autumn": bool(self.object.season & SeasonsSelectForm.SEASON_AUTUMN),
            "winter": bool(self.object.season & SeasonsSelectForm.SEASON_WINTER),
        }
        context["season_form"] = SeasonsSelectForm(initial=season_initial)
        # ItemPhotoモデルを参照し情報を取得
        context["photos"] = self.object.itemphoto_set.all()
        return context

    # ログインしているユーザーに紐づく削除されていないアイテムを抽出
    def get_queryset(self):
        user = self.request.user

        return Item.objects.filter(user=user, delete_flag=False)

    # requestをフォームに渡す
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request  # clean()がdelete_photosを参照できるように
        return kwargs

    # ユーザーがフォームを送信後、バリデーション通過後に行う保存や画面遷移処理のカスタマイズ
    def form_valid(self, form):
        # フォームから送られてきたデータをもとにitemオブジェクトを作成
        # 内容を加工後保存するため、一時保存。
        item = form.save(commit=False)

        # 入力に誤りがあった場合に呼び出される。form_invalidへオーバーライド
        season_form = SeasonsSelectForm(self.request.POST)
        if not season_form.is_valid():
            context = self.get_context_data(form=form, season_form=season_form)
            context["season_form"] = season_form
            return self.render_to_response(context)

        item.season = season_form.get_season_value()

        # description欄に記載がなければ、空文字にして表示。（Noneの表示を防ぐ）
        if item.description is None:
            item.description = ""

        # 加工後の内容を保存
        item.save()

        # 既存の削除
        delete_ids = self.request.POST.getlist("delete_photos")
        if delete_ids:
            ItemPhoto.objects.filter(id__in=delete_ids, item=item).delete()

        # 新規の保存
        for img in self.request.FILES.getlist("images"):
            # 画像の拡張子を取得し、空欄だった場合は.jpgを使用
            ext = os.path.splitext(img.name)[1] or ".jpg"

            # ユニークの名前をファイル名へ定義
            filename = f"items/{uuid.uuid4()}{ext}"

            # 「img」というファイルを読み込んで、保存できる形に変え、指定した名前で保存する
            saved_path = default_storage.save(filename, ContentFile(img.read()))

            # 保存したファイルの「アクセスできるURL」を作って、public_url に入れる
            public_url = default_storage.url(saved_path)

            # ItemPhotoモデルへ、itemへ紐づく画像のURLを登録する
            ItemPhoto.objects.create(item=item, url=public_url)

        # 詳細画面へリダイレクト
        return redirect("item-detail", pk=item.pk)
