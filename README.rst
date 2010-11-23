==================
Django Social Auth
==================

Django Social Auth is an easy to setup social authentication/registration
mechanism for Django projects.

Crafted using base code from django-twitter-oauth_ and django-openid-auth_,
implements a common interface to define new authentication providers from
third parties.


------------
Dependencies
------------
Dependencies that must be meet to use the app:

- OpenId support depends on python-openid_

- OAuth support depends on python-oauth_

- Twitter and Facebook support demands an application registration
  on their corresponding sites.


------------
Installation
------------
- Add social_auth app to PYTHONPATH and installed apps::

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

- Add desired authentication backends to AUTHENTICATION_BACKENDS_ setting::

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.TwitterOAuthBackend',
        'social_auth.backends.FacebookOAuthBackend',
        'social_auth.backends.OrkutOAuthBackend',
        'social_auth.backends.OpenIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

- Setup Twitter and Facebook keys (see OAuth_ section for details)::

    TWITTER_CONSUMER_KEY    = ''
    TWITTER_CONSUMER_SECRET = ''
    FACEBOOK_APP_ID         = ''
    FACEBOOK_API_SECRET     = ''
    ORKUT_CONSUMER_KEY      = ''
    ORKUT_CONSUMER_SECRET   = ''

- Setup login urls::

    LOGIN_URL          = '/login-form/'
    LOGIN_REDIRECT_URL = '/logged-in/'
    LOGIN_ERROR_URL    = '/login-error/'

  Check Django documentation at `Login url`_ and `Login redirect url`_

- Configure complete url name to avoid possible clashes::

    SOCIAL_AUTH_COMPLETE_URL_NAME = 'namespace:complete'

- Add urls entries::

    urlpatterns = patterns('',
        ...
        url(r'', include('social_auth.urls', namespace='social')),
        ...
    )

- Sync database to create needed models::

    ./manage syncdb

- Not mandatory, but recommended::

    SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

  or::

    import random
    SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])

  final user name will have an integer suffix in case it's already taken.

- OAuth authentication will store access_token by default, set this value
  to False to avoid such behavior::

    SOCIAL_AUTH_EXTRA_DATA = False

- It's possible to override the used User class if needed::

    SOCIAL_AUTH_USER_MODEL = 'myapp.CustomUser'

  this class must define the following fields::

    username   = CharField(...)
    email      = EmailField(...)
    password   = CharField(...)
    last_login = DateTimeField(blank=True)
    is_active  = BooleanField(...)

  and the methods::

    is_authenticated()

  AttributeError will be raised in case of any of these is
  missing, also the following are recommended but not enforced::

    first_name = CharField(...)
    last_name  = CharField(...)

  by default `auth.User`_ is used. Check example application for
  implementation details, but first, please take a look to `User Profiles`_,
  it might solve your case.


------
OpenId
------
OpenId support is simpler to implement than OAuth, by Google and Yahoo 
providers are supported by default, others are supported by POST method
providing endpoint Url.


-----
OAuth
-----
OAuth communication demands a set of keys exchange to validate the client
authenticity prior to user approbation. Twitter, Facebook and Orkut
facilitates these keys by application registration, see next sections for
details.


-------
Twitter
-------
Twitter offers per application keys named "Consumer Key" and
"Consumer Secret". To enable Twitter these two keys are needed.
Further documentation at `Twitter development resources`_:

- Register a new app at `Twitter App Creation`_,

- mark the "Yes, use Twitter for login" checkbox, and

- fill "Consumer Key" and "Consumer Secret" settings::

      TWITTER_CONSUMER_KEY
      TWITTER_CONSUMER_SECRET

- You don't need to specify the url callback


--------
Facebook
--------
Facebook works similar to Twitter but it's simpler to setup and
redirect url is passed as a parameter when issuing an authorization.
Further documentation at `Facebook development resources`_:

- Register a new app at `Facebook App Creation`_, and

- fill "App Id" and "App Secret" values in settings::

      FACEBOOK_APP_ID
      FACEBOOK_API_SECRET


-----
Orkut
-----
Orkut offers per application keys named "Consumer Key" and
"Consumer Secret". To enable Orkut these two keys are needed.

Check `Google support`_ and `Orkut API`_ for details on getting
your consumer_key and consumer_secret keys.

- fill "Consumer Key" and "Consumer Secret" settings::

      ORKUT_CONSUMER_KEY
      ORKUT_CONSUMER_SECRET


----
Bugs
----
Several, maybe, please report :-)


------------
Contributors
------------
Attributions to whom deserves:

- caioariede_ (Caio Ariede) 


----------
Copyrights
----------
Base work is copyrighted by:

- django-twitter-oauth::

    Original Copyright goes to Henrik Lied (henriklied)
    Code borrowed from https://github.com/henriklied/django-twitter-oauth

- django-openid-auth::

    django-openid-auth -  OpenID integration for django.contrib.auth
    Copyright (C) 2007 Simon Willison
    Copyright (C) 2008-2010 Canonical Ltd.

.. _django-twitter-oauth: https://github.com/henriklied/django-twitter-oauth
.. _django-openid-auth: https://launchpad.net/django-openid-auth
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _python-oauth: https://github.com/leah/python-oauth
.. _Login url: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-url
.. _Login redirect url: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-redirect-url
.. _Twitter development resources: http://dev.twitter.com/pages/auth
.. _Twitter App Creation: http://twitter.com/apps/new
.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/
.. _AUTHENTICATION_BACKENDS: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#authentication-backends
.. _auth.User: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py#L186
.. _User Profiles: http://www.djangobook.com/en/1.0/chapter12/#cn222
.. _caioariede: https://github.com/caioariede
.. _Google support: http://www.google.com/support/a/bin/answer.py?hl=en&answer=162105
.. _Orkut API:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
