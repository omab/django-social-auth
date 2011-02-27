import urllib
import urlparse
import unittest
from sgmllib import SGMLParser

from django.conf import settings
from django.test.client import Client
from django.core.urlresolvers import reverse

from social_auth.backends.twitter import TwitterAuth


SERVER_NAME = 'myapp.com'
SERVER_PORT = '8000'
USER   = 'social_auth'
PASSWD = 'pass(twitter).7'


class SocialAuthTestsCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(SocialAuthTestsCase, self).__init__(*args, **kwargs)

    def get_content(self, url, data=None):
        """Open URL and return content"""
        data = data and urllib.urlencode(data) or data
        return ''.join(urllib.urlopen(url, data=data).readlines())

    def reverse(self, name, backend):
        return reverse(name, args=(backend,))

    def make_relative(self, value):
        parsed = urlparse.urlparse(value)
        return urlparse.urlunparse(('', '', parsed.path, parsed.params,
                                    parsed.query, parsed.fragment))


class TwitterTestCase(SocialAuthTestsCase):
    def testLogin(self):
        response = self.client.get(self.reverse('begin', 'twitter'))
        # social_auth must redirect to service page
        self.assertEqual(response.status_code, 302)

        # Open first redirect page, it contains user login form because
        # we don't have cookie to send to twitter
        login_content = self.get_content(response['Location'])
        parser = FormParser('login_form')
        parser.feed(login_content)
        auth = {'session[username_or_email]': USER,
                'session[password]': PASSWD}

        # Check that action and values were loaded properly
        self.assertTrue(parser.action)
        self.assertTrue(parser.values)

        # Post login form, will return authorization or redirect page
        parser.values.update(auth)
        content = self.get_content(parser.action, data=parser.values)

        # If page contains a form#login_form, then we are in the app
        # authorization page because the app is not authorized yet,
        # otherwise the app already gained permission and twitter sends
        # a page that redirects to redirect_url
        if 'login_form' in content:
            # authorization form post, returns redirect_page
            parser = FormParser('login_form').feed(content)
            self.assertTrue(parser.action)
            self.assertTrue(parser.values)
            parser.values.update(auth)
            redirect_page = self.get_content(parser.action, data=parser.values)
        else:
            redirect_page = content

        parser = RefreshParser()
        parser.feed(redirect_page)
        self.assertTrue(parser.value)

        response = self.client.get(self.make_relative(parser.value))
        self.assertEqual(response.status_code, 302)
        location = self.make_relative(response['Location'])
        login_redirect = getattr(settings, 'LOGIN_REDIRECT_URL', '')
        self.assertTrue(location == login_redirect)

    def runTest(self):
        # don't run tests if it's not enabled
        if TwitterAuth.enabled:
            self.testLogin()


class TwitterParser(SGMLParser):
    def feed(self, data):
        SGMLParser.feed(self, data)
        self.close()
        return self


class FormParser(TwitterParser):
    def __init__(self, form_id, *args, **kwargs):
        TwitterParser.__init__(self, *args, **kwargs)
        self.form_id = form_id
        self.inside_form = False
        self.action = None
        self.values = {}

    def start_form(self, attributes):
        attrs = dict(attributes)
        if attrs.get('id') == self.form_id:
            self.inside_form = True
            self.action = attrs.get('action')

    def end_form(self):
        self.inside_form = False

    def start_input(self, attributes):
        attrs = dict(attributes)
        if self.inside_form:
            type, name, value = attrs.get('type'), attrs.get('name'), \
                                attrs.get('value')
            if name and value and type in ('text', 'hidden', 'password'):
                self.values[name] = value


class RefreshParser(TwitterParser):
    def __init__(self, *args, **kwargs):
        TwitterParser.__init__(self, *args, **kwargs)
        self.value = None

    def start_meta(self, attributes):
        attrs = dict(attributes)
        if attrs.get('http-equiv') == 'refresh':
            self.value = attrs.get('content').lstrip('0;url=')
