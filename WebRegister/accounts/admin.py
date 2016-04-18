# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
#
# from .models import Student
#
#
# # Register your models here.
#
# # 为 Student 模型定义一个 inline admin descriptor
# class StudentInline(admin.StackedInline):
#     model = Student
#     can_delete = False
#     verbose_name_plural = 'student'
#
#
# # 定义一个新的 User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (StudentInline,)
#
#
# # 重注册 UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import RegistrationInfoModel

admin.site.register(RegistrationInfoModel)
