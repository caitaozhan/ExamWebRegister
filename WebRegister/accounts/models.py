from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentInfoModel(models.Model):
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