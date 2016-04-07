from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home_page(request):
	return HttpResponse("主页")

def index(request):
    return HttpResponse("考试注册")
