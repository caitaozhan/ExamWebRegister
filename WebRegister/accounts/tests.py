from django.test import TestCase

signup_form_data = {
    'username': '王老菊',
    'password': '1234',
    'number': '20131001111',
    'gender': 'Male',
    'phone': '15822223333',
}

login_form_data = {
    'username': '王老菊',
    'password': '1234',
}

LoginURL = '/accounts/login'
SignupURL = '/accounts/signup'
ProfileURL = '/accounts/profile'


def response_is_html(response, title=None):
    test = TestCase()
    test.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
    if title is not None:
        test.assertContains(response, '<title>%s</title>' % (title,))
    test.assertTrue(response.content.endswith(b'</html>'))


class TestLoginView(TestCase):
    def create_user(self):
        self.client.post(SignupURL, data=signup_form_data)

    def test_can_return_login_page(self):
        response = self.client.get(LoginURL)
        response_is_html(response, title='login')

    def test_can_redirect_to_profile_page_when_succeed(self):
        self.create_user()
        response = self.client.post(LoginURL, data=login_form_data)
        self.assertRedirects(response, ProfileURL)


class TestSignupView(TestCase):
    def test_can_return_signup_page(self):
        response = self.client.get(SignupURL)
        response_is_html(response, title='signup')

    def test_can_redirect_to_login_page_when_finish_signup(self):
        response = self.client.post(SignupURL, data=signup_form_data)
        self.assertRedirects(response, LoginURL)

    def test_can_keep_former_input_when_failed_signup(self):
        response = self.client.post(SignupURL, data={'username': 'random_name'},
                                    follow=True)
        response_is_html(response, title='signup')
        self.assertContains(response, 'random_name')


class TestProfileView(TestCase):
    def create_user(self):
        self.client.post(SignupURL, data=signup_form_data)

    def login(self):
        self.client.post(LoginURL, data=login_form_data)

    def test_can_redirect_to_login_page_without_authorization(self):
        response = self.client.get(ProfileURL)
        self.assertRedirects(response, LoginURL + '?next=/accounts/profile')

    def test_can_return_profile_page_with_authorization(self):
        self.create_user()
        self.login()
        response = self.client.get(ProfileURL)
        response_is_html(response, title='profile')
        for value in (signup_form_data['username'],
                      signup_form_data['number'],
                      signup_form_data['phone']):
            self.assertContains(response, value)
