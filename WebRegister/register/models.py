from django.db import models
from django.utils import timezone


class ExamInfoModel(models.Model):
    subject = models.CharField(verbose_name="科目名称", max_length=30)
    exam_time = models.DateTimeField(verbose_name="考试开始时间")
    exam_time_end = models.DateTimeField(verbose_name="考试结束时间", default=timezone.now())
    place = models.CharField(verbose_name="考试地点", max_length=50)
    register_deadline = models.DateTimeField(verbose_name="报名截至时间", default=timezone.now)
    fee = models.IntegerField(verbose_name="考试费用")
    notes = models.CharField(verbose_name="备注", max_length=512, default="")

    class Meta:
        unique_together = (("subject", "exam_time", "place"),)  # 科目+时间+地点 -> 唯一确定一场考试
    # django 不支持 multi-column primary key, unique_together 是一种可行的“替代”方案
        # db_table = '"考试信息"'

    def __str__(self):
        return self.subject + " " + self.notes

