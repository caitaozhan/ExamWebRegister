from django import forms

from .models import ExamInfoModel, PlaceModel

EXAMS = ((exam.subject, exam.subject) for exam in ExamInfoModel.objects.all())
PLACES = ((place.place, place.place) for place in PlaceModel.objects.all())

# 自定义表单控件的属性
customize_attrs = {
    'class': 'form-control',  # Bootstrap 样式
}

GENDER_TYPE = (
    ('男', '男'),
    ('女', '女')
)


class ExaminationSelectForm(forms.Form):
    examination = forms.CharField(label="考试", max_length=30,
                                  widget=forms.Select(choices=EXAMS, attrs={'class': 'form-control'}))


class PlaceSelectForm(forms.Form):
    examination = forms.CharField(label="考试", max_length=30)
    place = forms.CharField(label="考试地点", max_length=32,
                            widget=forms.Select(choices=PLACES, attrs={'class': 'form-control'}))


class RegistrationForm(forms.Form):
    gender = forms.CharField(label="性别", max_length=6,
                             widget=forms.Select(choices=GENDER_TYPE, attrs=customize_attrs))
    phone = forms.CharField(label="手机号", max_length=20,
                            widget=forms.TextInput(attrs=customize_attrs))
    id_number = forms.CharField(label="身份证号", max_length=30,
                                widget=forms.TextInput(attrs=customize_attrs))
