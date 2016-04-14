from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import unittest


# Create your tests here.


class SignUpTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        pass

    def test_can_sign_up_a_user(self):
        self.browser.get('http://127.0.0.1:8000/register/signup')
        self.browser.find_element_by_name('username').send_keys('余宗福')
        self.browser.find_element_by_name('password').send_keys('1234abcd')
        self.browser.find_element_by_name('number').send_keys('20131001111')
        self.browser.find_element_by_name('gender').send_keys('Female')
        self.browser.find_element_by_name('phone').send_keys('18064097320')
        self.browser.find_element_by_name('submit').click()
