from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db.utils import IntegrityError

from .models import Student
from .forms import SignupForm, ProfileForm, LoginForm

from PIL import Image  # Python Image Library
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.


# 缩略图：宽度最大150， 长度最大210
def thumbnail_image(path):
    size = (150, 210)
    try:
        im = Image.open(path)
        im.thumbnail(size)
        im.save(path, "JPEG")
    except IOError:
        print("cannot not create thumbnail")


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.email = profile_form.cleaned_data['email']
            user.save()
            if hasattr(user, 'student'):
                stu = user.student
                stu.id_number = profile_form.cleaned_data['id_number']
                stu.gender = profile_form.cleaned_data['gender']
                stu.phone = profile_form.cleaned_data['phone']
                stu.head_image = profile_form.cleaned_data['head_image']
                stu.save()
                path = os.path.join(BASE_DIR, str(stu.head_image))
                thumbnail_image(path)
            return redirect(profile)
        else:
            return HttpResponse("profile form is not valid")
    else:  # request.POST == 'GET
        user = User.objects.get(username=request.user.username)
        if user.is_superuser:
            return redirect('/admin')
        user_profile = {  # 从数据库获取基本用户信息
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        if hasattr(user, 'student'):
            user_profile.update(user.student.profile_data())  # 从数据库获取用户的学生信息
        profile_form = ProfileForm(user_profile, auto_id=False)
    return render(request, 'profile.html', context={
        'username': request.user.username,  # username 不允许修改,分开表示
        'form': profile_form
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
                return redirect(log_in)
            except IntegrityError:
                pass
    else:
        user_form = SignupForm()
    return render(request, 'signup.html', {'form': user_form})
