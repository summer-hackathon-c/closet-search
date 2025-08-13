import os
import uuid
from django.views import View
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ItemCreateForm, PhotoUploadForm
from .models import Item, ItemPhoto
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# from .models import User

# Create your views here.


# ユーザー新規登録
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


# アイテム一覧
class ItemListView(ListView):
    model = Item
    template_name = "items/index.html"
    context_object_name = "items"


# アイテム新規登録
class ItemsCreateView(View):
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

        # (TODO)ログイン機能が実装されたら削除する
        dummy_user = User.objects.first()
        if dummy_user is None:
            messages.error(request, "ユーザーが存在しません。先に1件作成してください。")
            return render(
                request, self.template_name, {"form": form, "photo_form": photo_form}
            )

        # Itemモデルを保存（ユーザーとシーズンを設定）
        item = form.save(commit=False)
        item.user = dummy_user

        # (TODO)seasonは暫定で以下のように設定
        item.season = 0
        item.save()

        # アップロードされた複数画像を保存
        for img in request.FILES.getlist("images"):
            ext = os.path.splitext(img.name)[1].lower()
            filename = f"item_photos/{uuid.uuid4().hex}{ext}"
            saved_path = default_storage.save(filename, img)
            file_url = default_storage.url(saved_path)
            ItemPhoto.objects.create(item=item, url=file_url)

        # 一覧ページへリダイレクト
        return redirect("item-list")
