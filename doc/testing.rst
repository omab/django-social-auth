Testing
=======
Django-social-auth aims to be a fully tested project, some partial test are
present at the moment and others are being worked. 

To test the app just run::

    ./manage.py test social_auth

This will run a bunch of tests, so far only login process is tested, more
will come eventually.

User accounts on the different sites are needed to run tests, configure the
credentials in the following way::

    TEST_TWITTER_USER = 'testing_account'
    TEST_TWITTER_PASSWORD = 'password_for_testing_account'

    # facebook testing
    TEST_FACEBOOK_USER = 'testing_account'
    TEST_FACEBOOK_PASSWORD = 'password_for_testing_account'
