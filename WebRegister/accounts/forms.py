from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

# 自定义表单控件的属性
customize_attrs = {
    'class': 'form-control',  # Bootstrap 样式
}


# 用户登录表单
# 仅包含用户名和密码
class LoginForm(AuthenticationForm):
    # 相对于原声的 AuthenticationForm 表单, 定制了 widget 的样式
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput(attrs=customize_attrs))
    password = forms.CharField(label=_("Password"), strip=False,
                               widget=forms.PasswordInput(attrs=customize_attrs))


# 用户注册表单
# 仅包含注册时必须填写的信息
class SignupForm(forms.Form):
    GENDER_TYPE = (
        ('Male', '男'),
        ('Female', '女')
    )
    username = forms.CharField(label="用户名", max_length=30,
                               widget=forms.TextInput(attrs=customize_attrs))
    password = forms.CharField(label="密码", max_length=30,
                               widget=forms.PasswordInput(attrs=customize_attrs))
    number = forms.CharField(label="学号", max_length=30,
                             widget=forms.TextInput(attrs=customize_attrs))
    gender = forms.CharField(label="性别", max_length=6,
                             widget=forms.Select(attrs=customize_attrs,
                                                 choices=GENDER_TYPE))
    phone = forms.CharField(label="手机号", max_length=20,
                            widget=forms.TextInput(attrs=customize_attrs))


# 个人信息表单
# 包含所有可供用户查看和修改的信息
class ProfileForm(forms.Form):
    GENDER_TYPE = (
        ('男', '男'),
        ('女', '女')
    )
    # username = forms.CharField(label="用户名", max_length=30,
    #                            widget=forms.TextInput(attrs=customize_attrs))
    email = forms.EmailField(label="邮箱",
                             widget=forms.TextInput(attrs=customize_attrs))
    gender = forms.CharField(label="性别", max_length=6,
                             widget=forms.Select(choices=GENDER_TYPE,
                                                 attrs=customize_attrs))
    phone = forms.CharField(label="手机号", max_length=20,
                            widget=forms.TextInput(attrs=customize_attrs))
    number = forms.CharField(label="学号", max_length=30,
                             widget=forms.TextInput(attrs=customize_attrs))
