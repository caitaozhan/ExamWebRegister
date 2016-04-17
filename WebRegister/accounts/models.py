from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Todo: 为用户添加 "扩展记录", "附加信息". 使其能够动态的添加新的字段

class Student(models.Model):
    GENDER_TYPE = (
        ('男', '男'),
        ('女', '女')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.number

    def update_profile(self, new_profile):
        self.number = new_profile['number']
        self.gender = new_profile['gender']
        self.phone = new_profile['phone']

    def profile_data(self):
        return {
            'gender': self.gender,
            'number': self.number,
            'phone': self.phone,
        }
