from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.db.utils import IntegrityError
from django.views.decorators.http import require_safe

from .models import Student
from .forms import UserForm, ProfileForm


# Create your views here.

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            pass    # Todo: 使profile视图根据表单对数据库进行修改
    else:
        profile_dict = {
            'username': request.user.username,
            'gender': request.user.student.gender,
            'phone': request.user.student.phone,
            'number': request.user.student.number,
        } # Todo: 使其能够自动根据user,student,...的信息导入数据
        profile_form = ProfileForm(profile_dict)
    return render(request, 'profile.html', context={'form': profile_form})


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(profile)
            else:
                return render(request, 'base.html', {
                    'title': 'disabled_account',
                    'content': '<p class="lead">账号不可用</p>'
                })
        form = AuthenticationForm(request.POST)  #该语句似乎无效 #Todo: 使用户验证失败后显示错误信息并保留输入
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    return render(request, 'logout.html')


def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            try:
                new_user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                                    password=user_form.cleaned_data['password'])
                new_student = Student(user=new_user,
                                      number=user_form.cleaned_data['number'],
                                      gender=user_form.cleaned_data['gender'],
                                      phone=user_form.cleaned_data['phone'])
                new_student.save()
                return redirect(profile)
            except IntegrityError as e:
                pass
    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'form': user_form})
