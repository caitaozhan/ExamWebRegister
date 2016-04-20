from django import forms

from .models import ExamInfoModel

EXAMS = ((exam.subject, exam.subject) for exam in ExamInfoModel.objects.all())


class ExaminationSelectForm(forms.Form):
    examination = forms.CharField(label="考试", max_length=30,
                                  widget=forms.Select(choices=EXAMS, attrs={'class': 'form-control'}))
