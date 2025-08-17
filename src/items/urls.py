from django.urls import path
from django.views.generic import RedirectView
from .views import (
    SignUpView,
    UserLoginView,
    ItemCreateView,
    ItemListView,
    ItemDetailView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", RedirectView.as_view(url="/login/", permanent=False)),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<int:pk>", ItemDetailView.as_view(), name="item_detail"),
]
