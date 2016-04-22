from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import mark_safe
from django.utils.translation import ugettext_lazy as _

# 自定义表单控件的属性
customize_attrs = {
    'class': 'form-control',  # Bootstrap 样式
}

GENDER_TYPE = (
    ('男', '男'),
    ('女', '女')
)


# 用户登录表单
# 仅包含用户名和密码
class LoginForm(AuthenticationForm):
    # 相对于原声的 AuthenticationForm 表单, 定制了 widget 的样式
    username = forms.CharField(max_length=254, required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'inputtext',
                                   'placeholder': '用户名',
                                   'autofocus': '',
                               }))
    password = forms.CharField(label=_("Password"), required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'inputpassword',
                                   'placeholder': '密码',
                               }))


# 用户注册表单
# 仅包含注册时必须填写的信息
# Todo: username 已经注册过，重复注册失败，但是没有提示信息：“该用户名已经注册”
class SignupForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=30,
                               widget=forms.TextInput(attrs=customize_attrs))
    password = forms.CharField(label="密码", max_length=30,
                               widget=forms.PasswordInput(attrs=customize_attrs))
    id_number = forms.CharField(label="身份证号", max_length=30,
                                widget=forms.TextInput(attrs=customize_attrs))
    gender = forms.CharField(label="性别", max_length=6,
                             widget=forms.Select(attrs=customize_attrs,
                                                 choices=GENDER_TYPE))
    phone = forms.CharField(label="手机号", max_length=20,
                            widget=forms.TextInput(attrs=customize_attrs))


# 个人信息表单
# 包含所有可供用户查看和修改的信息
class ProfileForm(forms.Form):
    # username 不允许编辑, 不包含在表单中
    email = forms.EmailField(label="邮箱",
                             widget=forms.TextInput(attrs=customize_attrs),
                             required=False)
    gender = forms.CharField(label="性别", max_length=6,
                             widget=forms.Select(choices=GENDER_TYPE,
                                                 attrs=customize_attrs))
    phone = forms.CharField(label="手机号", max_length=20,
                            widget=forms.TextInput(attrs=customize_attrs))
    id_number = forms.CharField(label="身份证号", max_length=30,
                                widget=forms.TextInput(attrs=customize_attrs))
    head_image = forms.ImageField(label="头像")
