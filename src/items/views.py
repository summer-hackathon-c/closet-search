# from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm
from django.utils.timezone import now
# from .models import User

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
        return reverse_lazy("index")
