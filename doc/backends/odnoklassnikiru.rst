Odnoklassniki.ru
================

There are two options with Odnoklassniki: either you use OAuth2 workflow to
authenticate odnoklassniki users at external site, or you authenticate users
within your IFrame application.

OAuth
-----
If you use OAuth2 workflow, you need to:

- register a new application with `OAuth registration form`_
- fill out some settings::

    ODNOKLASSNIKI_OAUTH2_CLIENT_KEY = ''
    ODNOKLASSNIKI_OAUTH2_APP_KEY = ''
    ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET = ''

- add ``'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend'``
  into your ``AUTHENTICATION_BACKENDS``.

IFrame applications
-------------------

If you want to authenticate users in your IFrame application,

- read `Rules for application developers`_
- fill out `Developers registration form`_
- get your personal sandbox
- fill out some settings::

    ODNOKLASSNIKI_APP_ID = ''
    ODNOKLASSNIKI_APP_PUBLIC_KEY = ''
    ODNOKLASSNIKI_APP_SECRET = ''

- add ``'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiAppBackend'``
  into your ``AUTHENTICATION_BACKENDS``
- sign a public offer and do some bureaucracy

You may also use some options:

- ``ODNOKLASSNIKI_APP_EXTRA_USER_DATA_LIST`` (defaults to empty tuple), for the
  list of available fields see `Documentation on user.getInfo`_
- ``ODNOKLASSNIKI_SANDBOX_DEV_USERNAME`` and
  ``ODNOKLASSNIKI_SANDBOX_DEV_PASSWORD`` are username and password of your
  sandbox. They are only used in IFrame app testing
- ``ODNOKLASSNIKI_TEST_USERNAME`` and ``ODNOKLASSNIKI_TEST_PASSWORD`` should be
  username (or email) and password of real Odnoklassniki user. They are only
  used in OAuth testing.

.. _OAuth registration form: http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=13992188
.. _Rules for application developers: http://dev.odnoklassniki.ru/wiki/display/ok/Odnoklassniki.ru+Third+Party+Platform
.. _Developers registration form: http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=5668937
.. _Documentation on user.getInfo: http://dev.odnoklassniki.ru/wiki/display/ok/REST+API+-+users.getInfo
