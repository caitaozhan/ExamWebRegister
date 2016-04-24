from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import ExamInfoModel, PlaceModel
from .forms import ExaminationSelectForm, PlaceSelectForm, RegistrationForm

from accounts.models import RegistrationInfoModel


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
        # 验证表单中包含了所需的所有信息
        try:
            username = request.POST['username']
            examination = request.POST['examination']
            place = request.POST['place']
            gender = request.POST['gender']
            phone = request.POST['phone']
            id_number = request.POST['id_number']
        except KeyError:
            return render(request, 'error.html', context={'error_mes': '报名信息不全'})

        # 验证当前登录用户和当前表单中用户的一致性
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'error.html', context={'error_mes': '报名请求的用户不存在'})
        if request.user != user:
            return render(request, 'error.html', context={'error_mes': '报名用户和当前登录用户不符'})

        # 验证所提交的考试和地点可用,取出相应的 ExamInfoModel 和 PlaceModel 的对象
        try:
            # 自动选取该考试项目中时间最近的一次考试
            examination = ExamInfoModel.objects.order_by('exam_time').get(subject=examination)
            # 检查该考试项目是否过期
            if timezone.now() > examination.register_deadline:
                return render(request, 'error.html', context={'error_mes': '该考试项目以过期'})
            place = PlaceModel.objects.get(place=place)
        except ObjectDoesNotExist:
            return render(request, 'error.html', context={'error_mes': '考试项目或地点不存在'})

        # 保存考试注册的表单到数据库
        try:
            registration = RegistrationInfoModel(student=user.student,
                                                 exam=examination,
                                                 is_paid=False,
                                                 place=place)
            registration.generate_exam_number()  # 生成准考证号
            registration.save()
        except IntegrityError:
            return render(request, 'error.html', context={'error_mes': '无法保存表单到数据库'})

        # 最后验证数据库中确实存在该报名表
        try:
            RegistrationInfoModel.objects.get(student=user.student, exam=examination, place=place)
            return render(request, 'base.html', context={
                'title': 'registration_succeed',
                'content': '<p class="lead">报名成功</p>',
            })
        except RegistrationInfoModel.DoesNotExist:
            return render(request, 'error.html', context={'error_mes': '报名失败'})
    return render(request, 'error.html')


@login_required
def present_registration_form(request, username, examination, time, place):
    if request.POST == 'GET':
        # Todo: 显示相应的注册表单的信息
        pass
    else:
        # Todo: 显示错误信息并重定向
        pass
