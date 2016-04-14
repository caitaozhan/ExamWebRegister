from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def guide(request):
    return render(request, 'guide.html')
