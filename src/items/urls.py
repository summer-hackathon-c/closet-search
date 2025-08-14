from django.urls import path
from django.views.generic import RedirectView
from .views import SignUpView, UserLoginView, ItemCreateView, ItemListView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", RedirectView.as_view(url="/login/", permanent=False)),
    path("login/", UserLoginView.as_view(), name="login"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/", ItemListView.as_view(), name="item-list"),
]
