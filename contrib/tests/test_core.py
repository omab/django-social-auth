# -*- coding: utf-8 -*-
import urlparse

from selenium import webdriver

from django.test import TestCase
from django.conf import settings


class BackendsTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def url(self, path):
        return urlparse.urljoin(settings.TEST_DOMAIN, path)

    def test_twitter_backend(self):
        # We grab the Twitter testing user details from settings file
        TEST_TWITTER_USER = getattr(settings, 'TEST_TWITTER_USER', None)
        TEST_TWITTER_PASSWORD = getattr(settings, 'TEST_TWITTER_PASSWORD',
                                        None)
        self.assertTrue(TEST_TWITTER_USER)
        self.assertTrue(TEST_TWITTER_PASSWORD)

        self.driver.get(self.url('/login/twitter/'))

        # We log in
        username_field = self.driver.find_element_by_id('username_or_email')
        username_field.send_keys(TEST_TWITTER_USER)

        password_field = self.driver.find_element_by_id('password')
        password_field.send_keys(TEST_TWITTER_PASSWORD)
        password_field.submit()

        # The application might be already allowed
        try:
            self.driver.find_element_by_id('allow').click()
        except:
            pass

        # We check the user logged in
        heading = self.driver.find_element_by_id('heading')
        if not heading.text == u'Logged in!':
            raise Exception('The user didn\'t log in')

        # Here we could test the User's fields

    def test_google_oauth_backend(self):
        TEST_GOOGLE_USER = getattr(settings, 'TEST_GOOGLE_USER', None)
        TEST_GOOGLE_PASSWORD = getattr(settings, 'TEST_GOOGLE_PASSWORD', None)
        self.assertTrue(TEST_GOOGLE_USER)
        self.assertTrue(TEST_GOOGLE_PASSWORD)

        self.driver.get(self.url('/login/google-oauth/'))

        # We log in
        username_field = self.driver.find_element_by_id('Email')
        username_field.send_keys(TEST_GOOGLE_USER)

        password_field = self.driver.find_element_by_id('Passwd')
        password_field.send_keys(TEST_GOOGLE_PASSWORD)
        password_field.submit()

        # The application might be already allowed
        try:
            self.driver.find_element_by_id('allow').click()
        except:
            pass

        # We check the user logged in
        heading = self.driver.find_element_by_id('heading')
        if not heading.text == u'Logged in!':
            raise Exception('The user didn\'t log in')

        # Here we could test the User's fields

    def test_google_oauth2_backend(self):
        TEST_GOOGLE_USER = getattr(settings, 'TEST_GOOGLE_USER', None)
        TEST_GOOGLE_PASSWORD = getattr(settings, 'TEST_GOOGLE_PASSWORD', None)
        self.assertTrue(TEST_GOOGLE_USER)
        self.assertTrue(TEST_GOOGLE_PASSWORD)

        self.driver.get(self.url('/login/google-oauth2/'))

        # We log in
        username_field = self.driver.find_element_by_id('Email')
        username_field.send_keys(TEST_GOOGLE_USER)

        password_field = self.driver.find_element_by_id('Passwd')
        password_field.send_keys(TEST_GOOGLE_PASSWORD)
        password_field.submit()

        # The application might be already allowed
        try:
            self.driver.find_element_by_id('submit_approve_access').click()
        except:
            pass

        # We check the user logged in
        heading = self.driver.find_element_by_id('heading')
        if not heading.text == u'Logged in!':
            raise Exception('The user didn\'t log in')

        # Here we could test the User's fields

    def test_facebook_backend(self):
        TEST_FACEBOOK_USER = getattr(settings, 'TEST_FACEBOOK_USER', None)
        TEST_FACEBOOK_PASSWORD = getattr(settings, 'TEST_FACEBOOK_PASSWORD',
                                         None)
        self.assertTrue(TEST_FACEBOOK_USER)
        self.assertTrue(TEST_FACEBOOK_PASSWORD)

        self.driver.get(self.url('/login/facebook/'))

        # We log in
        username_field = self.driver.find_element_by_id('email')
        username_field.send_keys(TEST_FACEBOOK_USER)

        password_field = self.driver.find_element_by_id('pass')
        password_field.send_keys(TEST_FACEBOOK_PASSWORD)
        password_field.submit()

        try:
            self.driver.find_element_by_name('grant_clicked').click()
        except:
            pass

        # We check the user logged in
        heading = self.driver.find_element_by_id('heading')
        if not heading.text == u'Logged in!':
            raise Exception('The user didn\'t log in')

        # Here we could test the User's fields

    def test_linkedin_backend(self):
        TEST_LINKEDIN_USER = getattr(settings, 'TEST_LINKEDIN_USER', None)
        TEST_LINKEDIN_PASSWORD = getattr(settings, 'TEST_LINKEDIN_PASSWORD',
                                         None)
        self.assertTrue(TEST_LINKEDIN_USER)
        self.assertTrue(TEST_LINKEDIN_PASSWORD)

        self.driver.get(self.url('/login/linkedin/'))

        # We log in
        username_field = self.driver.find_element_by_id(
                                'session_key-oauthAuthorizeForm')
        username_field.send_keys(TEST_LINKEDIN_USER)

        password_field = self.driver.find_element_by_id(
                                'session_password-oauthAuthorizeForm')
        password_field.send_keys(TEST_LINKEDIN_PASSWORD)
        password_field.submit()

        # We check the user logged in
        heading = self.driver.find_element_by_id('heading')
        if not heading.text == u'Logged in!':
            raise Exception('The user didn\'t log in')

        # Here we could test the User's fields
