from django.shortcuts import render, redirect
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
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.email = profile_form.cleaned_data['email']
            user.student.update_profile(profile_form.cleaned_data)
            user.save()
            user.student.save()
            redirect(profile)
    else:
        user_profile = {
            'email': request.user.email,
        }
        student_profile = request.user.student.profile_data()
        user_profile.update(student_profile)
        # 构建表单
        profile_form = ProfileForm(user_profile)
    return render(request, 'profile.html', context={
        'username': request.user.username,  # username 不允许修改, 故特殊处理
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
                return render(request, 'base.html', {
                    'title': 'disabled_account',
                    'content': '<p class="lead">该账号不可用</p>'
                })
        login_form = LoginForm(cached_user_data)
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


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
                                      number=user_form.cleaned_data['number'],
                                      gender=user_form.cleaned_data['gender'],
                                      phone=user_form.cleaned_data['phone'])
                new_student.save()
                return redirect(profile)
            except IntegrityError as e:
                pass
    else:
        user_form = SignupForm()
    return render(request, 'signup.html', {'form': user_form})
