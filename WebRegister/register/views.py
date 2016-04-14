from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import ExamForm, UserForm
from .models import ExamInfoModel, StudentInfoModel

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("考试注册")


@login_required
def profile(request):
    if request.method == 'GET':
        profile = {
            'username': request.user.username,
            'number': request.user.studentinfomodel.number,
        }
        return render(request, 'registration/profile.html', context=profile)


def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            new_exam = ExamInfoModel(subject=form.cleaned_data['subject'],
                                     time=form.cleaned_data['time'],
                                     place=form.cleaned_data['place'],
                                     fee=form.cleaned_data['fee'])
            new_exam.save()
            return HttpResponse('新考试已保存.')
    else:
        form = ExamForm()
    return render(request, 'add_exam.html', {'form': form})


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password'])
            new_student = StudentInfoModel(user=new_user,
                                           number=form.cleaned_data['number'],
                                           gender=form.cleaned_data['gender'],
                                           phone=form.cleaned_data['phone'])
            new_student.save()
            return HttpResponse('新用户以保存')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})
