from django.urls import path
from .views import SignUpView, UserLoginView, ItemCreateView, ItemListView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/<int:user_id>/", ItemListView.as_view(), name="item-list"),
]
