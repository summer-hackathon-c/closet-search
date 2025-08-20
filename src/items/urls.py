from django.urls import path
from .views import (
    SignUpView,
    UserLoginView,
    RootRedirectView,
    ItemCreateView,
    ItemListView,
    ItemDetailView,
    ItemDeleteView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", RootRedirectView.as_view(), name="root-redirect"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<int:pk>", ItemDetailView.as_view(), name="item-detail"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
]
