from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import ExamInfoModel, PlaceModel

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
SelectForPlaceURL = reverse('select_for_place')
FillRegistrationFormURL = reverse('fill_registration_form')


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


class TestBeginRegistrationView(TestCase):
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

    def test_view_can_redirect_to_select_for_examination_page(self):
        response = self.client.get(BeginRegistrationURL)
        self.assertRedirects(response, SelectForExaminationURL)


class TestSelectForExaminationView(TestCase):
    """
    该视图仅接受 GET 方法, 并返回包含选择考试表单的 HTML
    """

    def setUp(self):
        self.client.post(SignupURL, data=signup_form_data)  # SignUp a new account
        self.client.post(LoginURL, data=login_form_data)  # Login

    def test_view_will_redirect_to_begin_registration_when_POST(self):
        # 设置 follow 为 True 将使其跟随重定向(而最终再次定位到本视图)
        response = self.client.post(SelectForExaminationURL, follow=True)
        self.assertRedirects(response, SelectForExaminationURL)

    def test_view_can_return_correct_html_when_GET(self):
        response = self.client.get(SelectForExaminationURL)
        response_is_html(response, title='select_for_examination')
        self.assertContains(response, '请选择考试项目')
        self.assertContains(response, '确定')


class TestSelectForPlaceView(TestCase):
    """
    该视图仅接受包含了合法的考试项目 POST 方法, 并返回包含选择考试地点表单的 HTML
    """

    def setUp(self):
        self.client.post(SignupURL, data=signup_form_data)  # SignUp a new account
        self.client.post(LoginURL, data=login_form_data)  # Login
        exam = ExamInfoModel(subject='AvailableExamination',
                             exam_time=timezone.now(),
                             fee=100, )  # 创建一个考试以供测试
        exam.save()

    def test_view_will_redirect_to_begin_registration_when_GET(self):
        response = self.client.get(SelectForPlaceURL, follow=True)
        self.assertRedirects(response, SelectForExaminationURL)

    def test_view_will_redirect_to_begin_registration_when_exam_incorrect(self):
        response = self.client.post(SelectForPlaceURL, follow=True, data={'examination': 'fuckFu'})
        self.assertRedirects(response, SelectForExaminationURL)

    def test_view_can_return_correct_html_when_exam_correct(self):
        response = self.client.post(SelectForPlaceURL, data={'examination': 'AvailableExamination'})
        response_is_html(response, title='select_for_place')
        self.assertContains(response, 'AvailableExamination')
        self.assertContains(response, '请选择考试地点')
        self.assertContains(response, '确定')


class TestFillRegistrationFormView(TestCase):
    """
    该视图仅接受包含了合法考试项目和考试地点 POST 方法, 并返回包含填写详细信息的表单的 HTML
    """

    def setUp(self):
        self.client.post(SignupURL, data=signup_form_data)  # SignUp a new account
        self.client.post(LoginURL, data=login_form_data)  # Login
        exam = ExamInfoModel(subject='AvailableExamination',
                             exam_time=timezone.now(),
                             fee=100, )  # 创建一个合法的考试以供测试
        place = PlaceModel(place='AvailablePlace')  # 创建一个合法的地点以供测试
        exam.save()
        place.save()

    def test_view_will_redirect_to_begin_registration_when_exam_incorrect(self):
        response = self.client.post(FillRegistrationFormURL, follow=True,
                                    data={'examination': 'fuckFu', 'place': 'AvailablePlace'})
        self.assertRedirects(response, SelectForExaminationURL)

    def test_view_will_redirect_to_begin_registration_when_place_incorrect(self):
        response = self.client.post(FillRegistrationFormURL, follow=True,
                                    data={'examination': 'AvailableExamination', 'place': 'fuckFu'})
        self.assertRedirects(response, SelectForExaminationURL)

    def test_view_can_return_correct_html_when_post_correct(self):
        response = self.client.post(FillRegistrationFormURL,
                                    data={'examination': 'AvailableExamination',
                                          'place': 'AvailablePlace'})
        response_is_html(response, title='fill_registration_form')
        self.assertContains(response, '请填写并确认报名表')
        # Todo: 验证页面中包含的足够详细的信息