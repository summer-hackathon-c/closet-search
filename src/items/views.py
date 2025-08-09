# from django.shortcuts import render
# from django.contrib.auth.views import LoginView
from django.views.generic import CreateView 
from django.urls import reverse_lazy 
from .forms import CustomUserCreationForm 
from .models import User

# Create your views here.

#新規登録 
class SignUpView(CreateView): 
    form_class = CustomUserCreationForm 
    template_name = "registration/signup.html" 
    success_url = reverse_lazy("login")