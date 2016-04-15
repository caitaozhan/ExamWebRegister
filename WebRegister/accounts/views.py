from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .models import StudentInfoModel
from .forms import UserForm


# Create your views here.

@login_required
def profile(request):
    if request.method == 'GET' and request.user.is_active:
        profile = {
            'username': request.user.username,
            'number': request.user.studentinfomodel.number,
            'gender': request.user.studentinfomodel.gender,
            'phone': request.user.studentinfomodel.phone,
        }
        return render(request, 'registration/profile.html', context=profile)
    return redirect(add_user)


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                    password=form.cleaned_data['password'])
                new_student = StudentInfoModel(user=new_user,
                                               number=form.cleaned_data['number'],
                                               gender=form.cleaned_data['gender'],
                                               phone=form.cleaned_data['phone'])
                new_student.save()
                return redirect(profile)
            except IntegrityError as e:
                pass
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})
