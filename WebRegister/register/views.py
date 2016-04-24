from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .models import ExamInfoModel, PlaceModel
from .forms import ExaminationSelectForm, PlaceSelectForm, RegistrationForm


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
            user = User.objects.get(username=request.user.username)
            # Todo: 确认用户可用, 考虑 superuser 的情况
            user_profile = {  # 获取基本用户信息
                'username': user.username,
                'email': user.email,
            }
            if hasattr(user, 'student'):
                user_profile.update(user.student.profile_data())  # 获取用户的学生信息
            registration_form = RegistrationForm(user_profile, auto_id=False)
        except ObjectDoesNotExist:
            return redirect(begin_registration)  # Todo: 增加错误信息显示
        return render(request, 'fill_registration_form.html', context={
            'username': user_profile['username'],
            'examination': examination.subject,
            'place': place.place,
            'form': registration_form,
        })
    else:
        return redirect(begin_registration)


@login_required
def save_registration_form(request):
    if request.method == 'POST':
        # Todo: 验证用户和当前表单的一致性
        # Todo: 验证所提交的考试和地点可用
        # Todo(optional): 验证当前用户个人信息和表单上个人信息的一致性
        # Todo: 选取考试时间(根据用户选定的考试中选择时间最近的)
        # Todo: 保存考试注册表单
        # Todo: 确定算法生成该报名表的准考号
        # Todo: if 顺利完成: 返回成功的页面
        # Todo: else: 返回错误页面(提示信息)
        pass


@login_required
def present_registration_form(request, username, examination, time, place):
    if request.POST == 'GET':
        # Todo: 显示相应的注册表单的信息
        pass
    else:
        # Todo: 显示错误信息并重定向
        pass
