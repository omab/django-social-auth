Testing
=======
Django-social-auth aims to be a fully tested project. Some partial tests are
present at the moment and others are being worked on.

To test the application just run::

    ./manage.py test social_auth

This will run a bunch of tests. So far only the login process is tested, but more
will come eventually.

User accounts on the different sites are needed to run tests, so configure the
credentials in the following way::

    TEST_TWITTER_USER = 'testing_account'
    TEST_TWITTER_PASSWORD = 'password_for_testing_account'

    # facebook testing
    TEST_FACEBOOK_USER = 'testing_account'
    TEST_FACEBOOK_PASSWORD = 'password_for_testing_account'

    # goole testing
    TEST_GOOGLE_USER = 'testing_account@gmail.com'
    TEST_GOOGLE_PASSWORD = 'password_for_testing_account'


There's support for Selenium_ tests too in the root contrib directory. To run,
install selenium::

    $ pip install selenium

and create a ``test_settings.py`` copying ``test_settings.py.template`` and
fill the needed account information. Then run::

    cd contrib/tests
    ./runtests.py

.. _Selenium: http://seleniumhq.org/
