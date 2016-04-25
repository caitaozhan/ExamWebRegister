from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import ExamInfoModel, PlaceModel
from accounts.models import RegistrationInfoModel
from .forms import ExaminationSelectForm, PlaceSelectForm, RegistrationForm
from .factories import create_registration


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
                user_profile.update(user.student.profile)  # 获取用户的学生信息
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
        try:
            username = request.POST['username']
            examination = request.POST['examination']
            place = request.POST['place']

            # gender = request.POST['gender']
            # phone = request.POST['phone']
            # id_number = request.POST['id_number']
            # Todo 用户在注册认为个人信息有误并提出修改是可以的

            # 验证用户
            user = User.objects.get(username=username)
            if request.user != user:
                return render(request, 'error.html', context={'error_mes': '报名用户和当前登录用户不符'})
            # 验证考试项目和地点
            examination = ExamInfoModel.objects.order_by('exam_time').get(subject=examination)

            if timezone.now() > examination.register_deadline:
                return render(request, 'error.html', context={'error_mes': '该考试项目以过期'})
            place = PlaceModel.objects.get(place=place)
            # 保存报名信息
            exam_number = create_registration({'student': user.student, 'examination': examination, 'place': place})
        except KeyError:
            return render(request, 'error.html', context={'error_mes': '报名信息不全'})
        except User.DoesNotExist:
            return render(request, 'error.html', context={'error_mes': '报名请求的用户不存在'})
        except ObjectDoesNotExist:  # ExamInfoModel.DoesNotExist and PlaceModel.DoesNotExist
            return render(request, 'error.html', context={'error_mes': '考试项目或地点不存在'})
        except IntegrityError:
            return render(request, 'error.html', context={'error_mes': '无法保存表单到数据库'})
        else:
            return render(request, 'registration_success.html', context={'exam_number': exam_number})
    return render(request, 'error.html')                                    # 依靠报名号，确定报名信息，从而打印出来


# , username, examination, time, place
@login_required
def print_registration_form(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.user.username)
            student = user.student
            exam_number = request.GET['exam_number']
            registration = RegistrationInfoModel.objects.get(exam_number=exam_number)

            is_paid = registration.is_paid
            place = registration.place

            return render(request, 'print_registration_form.html', context={'student': student.profile(),
                                                                            'exam': exam.print(),
                                                                            'exam_number': exam_number,
                                                                            'is_paid': is_paid,
                                                                            'place': place, })
        except:
            return render(request, 'error.html', context={'error_mes': '报名表打印错误'})
    else:
        # Todo: 显示错误信息并重定向
        return render(request, 'error.html', context={'error_mes': '不是GET方法'})
