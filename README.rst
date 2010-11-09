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
   * OpenId support depends on python-openid_
   * Twitter and Facebook support demands an application registration
     on their corresponding sites.


------------
Installation
------------

- Add social_auth app to your PYTHONPATH 

- Add social_auth application to your installed apps::

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

- Add desired authentication backends to AUTHENTICATION_BACKENDS setting::

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.TwitterOAuthBackend',
        'social_auth.backends.FacebookOAuthBackend',
        'social_auth.backends.OpenIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

- Setup Twitter and Facebook keys (see below)::

    TWITTER_CONSUMER_KEY    = ''
    TWITTER_CONSUMER_SECRET = ''
    FACEBOOK_APP_ID         = ''
    FACEBOOK_API_SECRET     = ''

- Setup login urls::

    LOGIN_URL          = '/login-form/'
    LOGIN_REDIRECT_URL = '/logged-in/'

  Check Django documentation at `Login url`_ and `Login redirect url`_


- Sync database to create needed models::

    ./manage syncdb


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
authenticity prior to user approbation, Twitter and Facebook facilitates these
keys by application registration.


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

Twitter demands a redirect url configuration and will force the user
to that address when redirecting, and http://127.0.0.1:8000 won't 
work. As a development hack, I suggest to setup something like
http://myvirtualapp.com and adding an entry in /etc/hosts for that
address pointing to localhost, port will be missed, but will do the
trick for testing.

If you cannot resit the missing port issue, play a bit with dnsmasq_.


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


----
Bugs
----
Several, maybe, please report :-)


----------
Copyrights
----------
Base work is copyrighted by:

django-twitter-oauth::

    Original Copyright goes to Henrik Lied (henriklied)
    Code borrowed from https://github.com/henriklied/django-twitter-oauth

django-openid-auth::

    django-openid-auth -  OpenID integration for django.contrib.auth
    Copyright (C) 2007 Simon Willison
    Copyright (C) 2008-2010 Canonical Ltd.

.. _django-twitter-oauth: https://github.com/henriklied/django-twitter-oauth
.. _django-openid-auth: https://launchpad.net/django-openid-auth
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _Login url: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-url
.. _Login redirect url: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-redirect-url
.. _Twitter development resources: http://dev.twitter.com/pages/auth
.. _Twitter App Creation: http://twitter.com/apps/new
.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/
