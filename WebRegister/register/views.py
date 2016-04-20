from django.shortcuts import render

from .models import ExamInfoModel

# Create your views here.

def examinations(request):
    return render(request, 'examinations.html',context={
        'exams': ExamInfoModel.objects.all(),
    })