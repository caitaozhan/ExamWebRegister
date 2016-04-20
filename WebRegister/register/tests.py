from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import ExamInfoModel

# Create your tests here.

signup_form_data = {
    'username': '王老菊',
    'password': '1234',
    'id_number': '342201199201034758',
    'gender': '男',
    'phone': '15822223333',
}

login_form_data = {
    'username': signup_form_data['username'],
    'password': signup_form_data['password'],
}

LoginURL = reverse('login')
SignupURL = reverse('signup')
ExaminationsURL = reverse('examinations')
BeginRegistrationURL = reverse('begin_registration')
SelectForExaminationURL = reverse('select_for_examination')


def response_is_html(response, title=None):
    test = TestCase()
    test.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
    if title is not None:
        test.assertContains(response, '<title>%s</title>' % (title,))
    test.assertTrue(response.content.endswith(b'</html>'))


class TestExaminationsView(TestCase):
    """
    测试 examinations 视图
    """

    def test_can_return_examinations_page(self):
        response = self.client.get(ExaminationsURL)
        response_is_html(response, title='examinations')
        for exam in ExamInfoModel.objects.all():
            self.assertContains(response, exam.subject)  # 测试页面是否包含了所有考试的 subject
            self.assertContains(response, exam.notes)  # 测试页面是否包含了所有考试的 notes


class TestRegisterViews(TestCase):
    """
    测试所有的 register 视图
    """

    def create_a_user(self):
        """
        使用 SignupURL 创建一个用户.
        :return None:
        """
        self.client.post(SignupURL, data=signup_form_data)

    def login(self):
        """
        使用 LoginURL 登录用户 (报考相关的所有页面都要求登录才能访问)
        :return None:
        """
        self.client.post(LoginURL, data=login_form_data)

    def setUp(self):
        self.create_a_user()
        self.login()

    def test_begin_registration_page_can_redirect_to_select_for_examination_page(self):
        response = self.client.get(BeginRegistrationURL)
        self.assertRedirects(response, SelectForExaminationURL)
