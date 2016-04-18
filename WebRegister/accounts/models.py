from django.db import models
from django.contrib.auth.models import User
from register.models import ExamInfoModel


# Create your models here.
# Todo: 为用户添加 "扩展记录", "附加信息". 使其能够动态的添加新的字段

class Student(models.Model):
    GENDER_TYPE = (
        ('男', '男'),
        ('女', '女')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 设为主码
    id_number = models.CharField(max_length=30, unique=True)                       # 身份证号
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    phone = models.CharField(max_length=20)
    exam = models.ManyToManyField(ExamInfoModel,
                                  through="RegistrationInfoModel",        # 表 RegistrationInfoModel 表示多对多关系
                                  through_fields=('student', 'exam'))

    def __str__(self):
        return self.user.username  # 返回名字

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


# 原来这个模型类在 register.models 里面，出现了 "from A import B, B import A" 的 bug
# 把 RegistrationInfoModel 放到 accounts.models 解决bug
# 毕竟决定把 Student 和 ExamInfoModel 之间的多对多关系 exam = models.ManyToManyField(ExamInfoModel,..) 放到Student模型里面
class RegistrationInfoModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)     # 外码
    exam = models.ForeignKey(ExamInfoModel, on_delete=models.CASCADE)  # 外码
    exam_number = models.CharField(max_length=30)                      # 准考证号
    is_paid = models.BooleanField(default=False)                       # 是否缴费

    def __str__(self):
        return self.subject + ':' + self.exam_number

