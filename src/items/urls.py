from django.urls import path
from django.views.generic import RedirectView
from .views import (
    SignUpView,
    UserLoginView,
    ItemCreateView,
    ItemListView,
    ItemDetailView,
    ItemDeleteView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", RedirectView.as_view(url="/login/", permanent=False)),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<int:pk>", ItemDetailView.as_view(), name="item-detail"),
    # TODO : 削除メソッド追加時、L22は削除してください。エラーにならないよう一旦Logoutに紐づけているだけですmm
    # path("<int:pk>/delete/", LogoutView.as_view(), name="item-delete"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
]
