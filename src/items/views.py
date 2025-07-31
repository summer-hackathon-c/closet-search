from django.http import HttpResponse


# from django.shortcuts import render
# (Ruffエラーのため上記コメントアウト)
# Create your views here.
def test(request):
    return HttpResponse("<h1> hello world</h1>")
