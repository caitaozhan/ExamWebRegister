from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ExamInfoModel


# Create your views here.

def examinations(request):
    return render(request, 'examinations.html', context={
        'exams': ExamInfoModel.objects.all(),
    })


@login_required
def begin_registration(request):
    return render(request, 'base.html', context={
        'title': 'begin_registration',
        'content': '<p  class="lead">请选择考试项目</p>',
    })


@login_required
def register_for_selected_exam(request):
    pass


@login_required
def register_for_selected_exam_and_place(request):
    pass


@login_required
def fill_registration_form(request):
    pass
