from django import forms

from .models import ExamInfoModel, PlaceModel

EXAMS = ((exam.subject, exam.subject) for exam in ExamInfoModel.objects.all())
PLACES = ((place.place, place.place) for place in PlaceModel.objects.all())


class ExaminationSelectForm(forms.Form):
    examination = forms.CharField(label="考试", max_length=30,
                                  widget=forms.Select(choices=EXAMS, attrs={'class': 'form-control'}))


class PlaceSelectForm(forms.Form):
    examination = forms.CharField(label="考试", max_length=30)
    place = forms.CharField(label="考试地点", max_length=32,
                            widget=forms.Select(choices=PLACES, attrs={'class': 'form-control'}))
