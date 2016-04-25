from accounts.models import RegistrationInfoModel

from .exceptions import MainInfoLack


def create_registration(data):
    try:
        registration = RegistrationInfoModel(student=data['student'],
                                             exam=data['examination'],
                                             is_paid=False,
                                             place=data['place'])
        exam_number = registration.generate_exam_number()  # 生成准考证号
        registration.save()
    except KeyError as key:
        raise MainInfoLack('创建考试注册表的数据不足, 需要%s, 但没有找到' % key)
    else:
        return exam_number
