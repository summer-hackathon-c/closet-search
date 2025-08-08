from django.urls import path
from . import views
from .views import SignUpView


urlpatterns = [
    # path("",views.test),
    path("signup/",SignUpView.as_view(), name="signup")
]
