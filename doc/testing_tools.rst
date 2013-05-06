Testing Tools
=============

django social auth provides an extension of Django's test client, SocialClient.
SocialClient provides the ability for a unit test to authenticate a user
through facebook. All calls to facebook are mocked. This is helpful for 
performing integration tests of the authentication pipeline or accessing 
a view that requires a user to be logged in.

Example:

.. code-block:: python

    from django.test import TestCase
    from social_auth.tests.client import SocialClient

    class SomeTestClass(TestCase):

        client = SocialClient
        user = {
            'first_name': 'Django',
            'last_name': 'Reinhardt',
            'verified': True,
            'name': 'Django Reinhardt',
            'locale': 'en_US',
            'hometown': {
                'id': '12345678',
                'name': 'Any Town, Any State'
            },
            'expires': '4812',
            'updated_time': '2012-01-29T19:27:32+0000',
            'access_token': 'dummyToken',
            'link': 'http://www.facebook.com/profile.php?id=1234',
            'location': {
                'id': '108659242498155',
                'name': 'Chicago, Illinois'
            },
            'gender': 'male',
            'timezone': -6,
            'id': '1234',
            'email': 'user@domain.com'
        }

        def test_something(self):
            self.client.login(self.user, backend='facebook')
            # do something with the logged in user.
