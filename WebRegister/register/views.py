from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate


from .forms import ExamForm
from .models import ExamInfoModel

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("考试注册")


def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            new_exam = ExamInfoModel(subject=form.cleaned_data['subject'],
                                     time=form.cleaned_data['time'],
                                     place=form.cleaned_data['place'],
                                     fee=form.cleaned_data['fee'])
            new_exam.save()
            return HttpResponse('新考试已保存.')
    else:
        form = ExamForm()
    return render(request, 'add_exam.html', {'form': form})
