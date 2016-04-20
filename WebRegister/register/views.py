from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ExamInfoModel
from .forms import ExaminationSelectForm


# Create your views here.

def examinations(request):
    return render(request, 'examinations.html', context={
        'exams': ExamInfoModel.objects.all(),
    })


@login_required
def begin_registration(request):
    """报名考试的入口视图, 重定向到 select_for_examination 视图"""
    return redirect(select_for_examination)


@login_required
def select_for_examination(request):
    """引导用户选择考试项目, 当用户选中考试地区后重定向到 select_for_place 视图"""
    if request.method == 'GET':
        return render(request, 'select_for_examination.html', context={
            'form': ExaminationSelectForm()['examination'],
        })
    # elif request.method == 'POST':
    #     examination = request.POST['examination']
    #     if ExamInfoModel.objects.get(subject=examination) is not None:
    #         return redirect(select_for_place, examination=examination)
    #     return redirect(select_for_examination)
    else:
        return redirect(begin_registration)


@login_required
def select_for_place(request):
    """引导用户选择考试项目, 当确保用户同时选中考试项目和地点时重定向到 fill_registration_form 视图"""
    pass


@login_required
def fill_registration_form(request):
    pass
