# from django.shortcuts import render
# from django.contrib.auth.views import LoginView
import os
import uuid
from django.views import View
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm,ItemForm, PhotoUploadForm
from .models import Item,ItemPhoto
from django.contrib.auth import get_user_model
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
    context_object_name = "item"
    
# アイテム新規登録
class ItemsCreateView(View):
    template_name = "items/create.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": ItemForm(),
            "photo_form": PhotoUploadForm(),
        })

    def post(self, request):
        form = ItemForm(request.POST)
        photo_form = PhotoUploadForm(request.POST, request.FILES)

        if form.is_valid() and photo_form.is_valid():
            # アイテム作成（modelsは user_id というFK名）
            item = form.save(commit=False)
            # ★ ログイン機能未完成なので一時的に固定ユーザーを紐づけ
            # item.user_id = request.user  # ← 本来はこちら
            item.user_id = User.objects.first()  # 先頭ユーザーを仮で設定
            
            # ★ 必須カラム season をデフォルトで補完（0 など）
            item.season = 0
            item.save()

            # 画像を複数保存
            for img in request.FILES.getlist("images"):
                ext = os.path.splitext(img.name)[1].lower()
                filename = f"item_photos/{uuid.uuid4().hex}{ext}"
                saved_path = default_storage.save(filename, img)
                file_url = default_storage.url(saved_path)  # 例: /media/item_photos/xxxx.jpg
                ItemPhoto.objects.create(item_id=item, url=file_url)

            return redirect("item-list")

        return render(request, self.template_name, {
            "form": form,
            "photo_form": photo_form,
        })
