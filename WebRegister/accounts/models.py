from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Todo 1: 修改用户模型,使其使用邮箱为唯一确定的账号
# Todo 2: 考虑能够为一个用户赋予不同的身份场景(学生,军官...)
# Todo 3: 为用户添加 "扩展记录", "附加信息". 使其能够动态的添加新的字段

class Student(models.Model):
    GENDER_TYPE = (
        ('男', '男'),
        ('女', '女')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # school_name = models.CharField(max_length=20)
    number = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.number
