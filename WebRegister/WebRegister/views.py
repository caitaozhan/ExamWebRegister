from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def guide(request):
    return render(request, 'guide.html', context={
        # 'autoescape off' needed
        'indent': '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;',
        'larger_indent': '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;',
    })
