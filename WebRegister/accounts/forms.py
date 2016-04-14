from django import forms

class UserForm(forms.Form):
    GENDER_TYPE = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female')
    )

    username = forms.CharField(label="用户名", max_length=10,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    number = forms.CharField(label="学号", max_length=30,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(label="性别", max_length=6,
                             widget=forms.Select(choices=GENDER_TYPE,
                                                 attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号", max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))