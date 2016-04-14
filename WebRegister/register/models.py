from django.db import models
from django.contrib.auth.models import User


class ExamInfoModel(models.Model):
    subject = models.CharField(max_length=30)
    time = models.DateTimeField()
    place = models.CharField(max_length=50)
    fee = models.IntegerField()

    def __str__(self):
        return self.subject


class RegistrationInfoModel(models.Model):
    exam_number = models.CharField(max_length=30)
    subject = models.ForeignKey(ExamInfoModel, default=None)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.subject + ':' + self.exam_number


class StudentInfoModel(models.Model):
    GENDER_TYPE = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.number
