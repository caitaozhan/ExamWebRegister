from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import ExamInfoModel, PlaceModel
from .forms import ExaminationSelectForm, PlaceSelectForm


# Create your views here.

def examinations(request):
    return render(request, 'examinations.html', context={
        'exams': ExamInfoModel.objects.all(),
    })


@login_required
def begin_registration(request):
    """报名考试的入口视图, 直接重定向到 select_for_examination 视图"""
    return redirect(select_for_examination)


@login_required
def select_for_examination(request):
    """引导用户选择考试项目, 当用户选中考试地区后重定向到 select_for_place 视图"""
    if request.method == 'GET':
        return render(request, 'select_for_examination.html', context={
            'form': ExaminationSelectForm()['examination'],
        })
    else:
        return redirect(begin_registration)


@login_required
def select_for_place(request):
    """引导用户选择考试项目, 当确保用户同时选中考试项目和地点时重定向到 fill_registration_form 视图"""
    if request.method == 'POST':
        try:
            examination = ExamInfoModel.objects.get(subject=request.POST['examination'])
        except ExamInfoModel.DoesNotExist:
            return redirect(begin_registration)  # Todo: 增加错误信息显示
        return render(request, 'select_for_place.html', context={
            'examination': examination,
            'place': PlaceSelectForm()['place'],
        })
    else:
        return redirect(begin_registration)


@login_required
def fill_registration_form(request):
    if request.method == 'POST':
        try:
            examination = ExamInfoModel.objects.get(subject=request.POST['examination'])
            place = PlaceModel.objects.get(place=request.POST['place'])
        except ObjectDoesNotExist:
            return redirect(begin_registration)  # Todo: 增加错误信息显示
        return render(request, 'fill_registration_form.html')
    else:
        return redirect(begin_registration)
