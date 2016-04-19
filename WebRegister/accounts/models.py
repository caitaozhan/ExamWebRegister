from django.db import models
from django.contrib.auth.models import User
from register.models import ExamInfoModel

GENDER_TYPE = (
    ('男', '男'),
    ('女', '女')
)


# Create your models here.
# Todo: 为用户添加 "扩展记录", "附加信息". 使其能够动态的添加新的字段

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 设为主码
    id_number = models.CharField(max_length=30, unique=True)  # 身份证号
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    phone = models.CharField(max_length=20)
    exam = models.ManyToManyField(ExamInfoModel,
                                  through="RegistrationInfoModel",  # 表 RegistrationInfoModel 表示多对多关系
                                  through_fields=('student', 'exam'))

    def __str__(self):
        return self.user.username  # 返回名字

    def update_profile(self, new_profile):
        """
        更新 Student 数据库的信息 (不应出现不希望用户更改的数据)
        :param new_profile:
        :return None:
        """
        self.id_number = new_profile['id_number']
        self.gender = new_profile['gender']
        self.phone = new_profile['phone']
        self.save()  # 保存数据

    def profile_data(self):
        """
        获取用户的 profile (应包含所有的希望显示在 profile 页面的个人信息)
        :return profile_data:
        """
        return {
            'username': self.user.username,
            'email': self.user.email,
            'id_number': self.id_number,
            'gender': self.gender,
            'phone': self.phone,
        }


# 原来这个模型类在 register.models 里面，出现了 "from A import B, B import A" 的 bug
# 把 RegistrationInfoModel 放到 accounts.models 解决bug
# 毕竟决定把 Student 和 ExamInfoModel 之间的多对多关系 exam = models.ManyToManyField(ExamInfoModel,..) 放到Student模型里面
class RegistrationInfoModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # 外码
    exam = models.ForeignKey(ExamInfoModel, on_delete=models.CASCADE)  # 外码
    exam_number = models.CharField(max_length=30)  # 准考证号
    is_paid = models.BooleanField(default=False)  # 是否缴费

    def __str__(self):
        return self.subject + ':' + self.exam_number
