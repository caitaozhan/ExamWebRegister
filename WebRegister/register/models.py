from django.db import models
from django.utils import timezone


class ExamInfoModel(models.Model):
    subject = models.CharField(verbose_name="科目名称", max_length=30)
    exam_time = models.DateTimeField(verbose_name="考试开始时间")
    exam_time_end = models.DateTimeField(verbose_name="考试结束时间", default=timezone.now)
    register_deadline = models.DateTimeField(verbose_name="报名截至时间", default=timezone.now)
    fee = models.IntegerField(verbose_name="考试费用")
    notes = models.CharField(verbose_name="备注", max_length=512, default="")

    class Meta:
        unique_together = (("subject", "exam_time"),)  # 科目+时间+地点 -> 唯一确定一场考试
    # django 不支持 multi-column primary key, unique_together 是一种可行的“替代”方案

    def __str__(self):
        return self.subject


# 这个表里面保存了上百个大学，作为考试地点
class PlaceModel(models.Model):
    place = models.CharField(verbose_name="考试地点", max_length=32, primary_key=True)

    def __str__(self):
        return self.place
