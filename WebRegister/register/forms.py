from django import forms


class ExamForm(forms.Form):
    subject = forms.CharField(label="课程", max_length=30,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    time = forms.DateTimeField(label="考试时间",
                               widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    # place = forms.CharField(label="考试地点", max_length=50,
                           # widget=forms.TextInput(attrs={'class': 'form-control'}))
    fee = forms.IntegerField(label="报考费用",
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
