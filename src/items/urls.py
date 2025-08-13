from django.urls import path
from .views import SignUpView, UserLoginView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
]
