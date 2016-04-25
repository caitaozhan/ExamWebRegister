from django.contrib.auth.models import User

from .models import Student
from .exceptions import MainInfoLack


def create_student(data):
    try:
        new_user = User.objects.create_user(username=data['username'],
                                            password=data['password'])
        new_student = Student(user=new_user,
                              id_number=data['id_number'],
                              gender=data['gender'],
                              phone=data['phone'])
        new_student.save()
    except KeyError as key:
        raise MainInfoLack('创建学生对象的数据不足, 需要%s, 但没有找到' % key)
