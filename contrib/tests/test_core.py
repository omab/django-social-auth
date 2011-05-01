# -*- coding: utf-8 -*-
from selenium import webdriver

from django.test import TestCase
from django.conf import settings


class BackendsTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_twitter_backend(self):
        # We grab the Twitter testing user details from settings file
        TEST_TWITTER_USER = getattr(settings, 'TEST_TWITTER_USER', None)
        TEST_TWITTER_PASSWORD = getattr(settings, 'TEST_TWITTER_PASSWORD', None)
        self.assertTrue(TEST_TWITTER_USER)
        self.assertTrue(TEST_TWITTER_PASSWORD)

        self.driver.get("http://social.matiasaguirre.net/login/twitter/")

        # We log in
        username_field = self.driver.find_element_by_id("username_or_email")
        username_field.send_keys(TEST_TWITTER_USER)

        password_field = self.driver.find_element_by_id("session[password]")
        password_field.send_keys(TEST_TWITTER_PASSWORD)
        password_field.submit()

        # The application might be already allowed
        try:
            self.driver.find_element_by_id("allow").click()
        except:
            pass

        # We check the user logged in
        heading = self.driver.find_element_by_id("heading")
        if not heading.text == u'Logged in!':
            raise Exception("The user didn't logged in")

        # Here we could test the User's fields
