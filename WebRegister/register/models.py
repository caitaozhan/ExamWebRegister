from django.db import models


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
