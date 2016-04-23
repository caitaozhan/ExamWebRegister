from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db.utils import IntegrityError

from .models import Student
from .forms import SignupForm, ProfileForm, LoginForm


# Create your views here.


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.email = profile_form.cleaned_data['email']
            user.save()
            if hasattr(user, 'student'):
                user.student.update_profile(profile_form.cleaned_data)
            return redirect(profile)
        else:
            return HttpResponse("profile form is not valid")  # 如果表单里面不填写头像，则表单not valid
    else:  # request.POST == 'GET
        user = User.objects.get(username=request.user.username)
        if user.is_superuser:
            return redirect('/admin')
        user_profile = {  # 获取基本用户信息
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        if hasattr(user, 'student'):
            user_profile.update(user.student.profile_data())  # 获取用户的学生信息
        profile_form = ProfileForm(user_profile, auto_id=False)
    return render(request, 'profile.html', context={
        'username': request.user.username,
        'form': profile_form,
        'head_image_file':
            user_profile['head_image'] if 'head_image' in user_profile else '',  # 指定头像文件的位置
    })


def log_in(request):
    if request.method == 'POST':
        cached_user_data = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }
        user = authenticate(username=cached_user_data['username'],
                            password=cached_user_data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(profile)
            else:
                return render(request, 'base.html', context={
                    'title': 'disabled_account',
                    'content': '<p class="lead">该账号不可用</p>'
                })
        login_form = LoginForm(cached_user_data)
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {
        'username': login_form['username'],
        'password': login_form['password'],
    })


@login_required
def log_out(request):
    logout(request)
    return render(request, 'logout.html')


def sign_up(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            try:
                new_user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                                    password=user_form.cleaned_data['password'])
                new_student = Student(user=new_user,
                                      id_number=user_form.cleaned_data['id_number'],
                                      gender=user_form.cleaned_data['gender'],
                                      phone=user_form.cleaned_data['phone'])
                new_student.save()
                return redirect(log_in)  # Todo: 存在新用户学生信息无法保存的 bug ?
            except IntegrityError:
                pass
    else:
        user_form = SignupForm()
    return render(request, 'signup.html', {'form': user_form})
