from django.db import models
from django.utils import timezone
# from accounts.models import Student


class ExamInfoModel(models.Model):
    subject = models.CharField(max_length=30)   # 科目名称
    exam_time = models.DateTimeField()          # 考试时间
    place = models.CharField(max_length=50)     # 考试地点
    register_deadline = models.DateTimeField(default=timezone.now)  # 报名截至时间。如果没有默认时间，则无法添加新的一列
    fee = models.IntegerField()                 # 考试费用

    class Meta:
        unique_together = (("subject", "exam_time", "place"),)  # 科目+时间+地点 -> 唯一确定一场考试
    # django 不支持 multi-column primary key, unique_together 是一种可行的“替代”方案

    def __str__(self):
        return self.subject

