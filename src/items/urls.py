from django.urls import path
from .views import SignUpView, ItemCreateView, ItemListView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/", ItemListView.as_view(), name="item-list"),
]
