import re

from social_auth.utils import setting
from social_auth.tests.base import SocialAuthTestsCase, FormParserByID


class FacebookTestCase(SocialAuthTestsCase):
    SERVER_NAME = 'myapp.com'
    SERVER_PORT = '8000'
    name = 'facebook'

    def setUp(self, *args, **kwargs):
        super(FacebookTestCase, self).setUp(*args, **kwargs)
        self.user = setting('TEST_FACEBOOK_USER')
        self.passwd = setting('TEST_FACEBOOK_PASSWORD')
        # check that user and password are setup properly
        self.assertTrue(self.user)
        self.assertTrue(self.passwd)


REDIRECT_RE = re.compile('window.location.replace\("(.*)"\);')


class FacebookTestLogin(FacebookTestCase):
    def test_login_succeful(self):
        response = self.client.get(self.reverse('socialauth_begin',
                                                'facebook'))
        # social_auth must redirect to service page
        self.assertEqual(response.status_code, 302)

        # Open first redirect page, it contains user login form because
        # we don't have cookie to send to twitter
        parser = FormParserByID('login_form')
        parser.feed(self.get_content(response['Location'], use_cookies=True))
        auth = {'email': self.user,
                'pass': self.passwd}

        # Check that action and values were loaded properly
        self.assertTrue(parser.action)
        self.assertTrue(parser.values)

        # Post login form, will return authorization or redirect page
        parser.values.update(auth)
        content = self.get_content(parser.action, parser.values,
                                   use_cookies=True)

        # If page contains a form#login_form, then we are in the app
        # authorization page because the app is not authorized yet,
        # otherwise the app already gained permission and twitter sends
        # a page that redirects to redirect_url
        if 'uiserver_form' in content:
            # authorization form post, returns redirect_page
            parser = FormParserByID('uiserver_form').feed(content)
            self.assertTrue(parser.action)
            self.assertTrue(parser.values)
            parser.values.update(auth)
            redirect_page = self.get_content(parser.action, parser.values,
                                             use_cookies=True)
        else:
            redirect_page = content

        url = REDIRECT_RE.findall(redirect_page)
        self.assertTrue(url)
        # URL comes on JS scaped, needs to be clean first, any better way?
        url = url[0].replace('\u0025', '%').replace('\\', '')
        response = self.client.get(self.make_relative(url))
