==================
Django Social Auth
==================

Django Social Auth is an easy to setup social authentication/authorization
mechanism for Django projects.

Crafted using base code from django-twitter-oauth_ and django-openid-auth_,
implements a common interface to define new authentication providers from
third parties.


----
Demo
----
There's a demo at http://social.matiasaguirre.net/, it lacks Orkut support
at the moment.


--------
Features
--------
This application provides user registration and login using social sites
credentials, some features are:

- Registration and Login using social sites using the following providers
  at the moment:

    * `Google OpenID`_
    * `Google OAuth`_
    * `Yahoo OpenID`_
    * OpenId_ like myOpenID_
    * `Twitter OAuth`_
    * `Facebook OAuth`_

  Some contributions added support for:

    * `LiveJournal OpenID`_
    * `Orkut OAuth`_

- Basic user data population and signaling, to allows custom fields values
  from providers response

- Multiple social accounts association to single users

- Custom User model override if needed (`auth.User`_ by default)


------------
Dependencies
------------
Dependencies that must be meet to use the app:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on python-oauth_

- Twitter and Facebook support demands an application registration
  on their corresponding sites.


------------
Installation
------------

From pypi_::

    $ pip install django-social-auth

or::

    $ easy_install django-social-auth

or clone from github_::

    $ git clone git://github.com/omab/django-social-auth.git

and add social_auth to PYTHONPATH::

    $ export PYTHONPATH=$PYTHONPATH:$(pwd)/django-social-auth/

or::

    $ cd django-social-auth
    $ sudo python setup.py install


-------------
Configuration
-------------
- Add social_auth to PYTHONPATH and installed applications::

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

- Add desired authentication backends to AUTHENTICATION_BACKENDS_ setting::

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.twitter.TwitterBackend',
        'social_auth.backends.facebook.FacebookBackend',
        'social_auth.backends.google.GoogleOAuthBackend',
        'social_auth.backends.google.GoogleBackend',
        'social_auth.backends.yahoo.YahooBackend',
        'social_auth.backends.contrib.LiveJournalBackend',
        'social_auth.backends.contrib.orkut.OrkutBackend',
        'social_auth.backends.OpenIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

  Note: this was introduced in a recent change and it's not backward
  compatible, take into account that saved sessions won't be able to login
  because the backend string stored in session (like backends.TwitterBackend)
  won't match the new paths.

- The app will try to import custom backends from the sources defined in::

    SOCIAL_AUTH_IMPORT_BACKENDS = (
        'myproy.social_auth_extra_services',
    )

  This way it's easier to add new providers, check the already defined ones
  in social_auth.backends for examples.

  Take into account that backends must be defined in AUTHENTICATION_BACKENDS_
  or Django won't pick them when trying to authenticate the user.

- Setup Twitter, Facebook, Orkut and Google OAuth keys (see OAuth_ section
  for details)::

    TWITTER_CONSUMER_KEY     = ''
    TWITTER_CONSUMER_SECRET  = ''
    FACEBOOK_APP_ID          = ''
    FACEBOOK_API_SECRET      = ''
    ORKUT_CONSUMER_KEY       = ''
    ORKUT_CONSUMER_SECRET    = ''
    GOOGLE_CONSUMER_KEY      = ''
    GOOGLE_CONSUMER_SECRET   = ''

- Setup login URLs::

    LOGIN_URL          = '/login-form/'
    LOGIN_REDIRECT_URL = '/logged-in/'
    LOGIN_ERROR_URL    = '/login-error/'

  Check Django documentation at `Login URL`_ and `Login redirect URL`_

- Configure authentication and association complete URL names to avoid
  possible clashes::

    SOCIAL_AUTH_COMPLETE_URL_NAME  = 'complete'
    SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'associate_complete'

- Add URLs entries::

    urlpatterns = patterns('',
        ...
        url(r'', include('social_auth.urls')),
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

- OAuth_ authentication will store access_token by default, set this value
  to False to avoid such behavior::

    SOCIAL_AUTH_EXTRA_DATA = False

- It's possible to override the used User model if needed::

    SOCIAL_AUTH_USER_MODEL = 'myapp.CustomUser'

  This class *must* have a custom `Model Manager`_ with a create_user method
  that resembles the one on `auth.UserManager`_.

  Also, it's highly recommended that this class define the following fields::

    username   = CharField(...)
    last_login = DateTimeField(blank=True)
    is_active  = BooleanField(...)

  and the method::

    is_authenticated():
        ...

  These are needed to ensure a better django-auth integration, in other case
  `login_required`_ won't be usable. A warning is displayed if any of these are
  missing. By default `auth.User`_ is used.

  Check example application for implementation details, but first, please take
  a look to `User Profiles`_, it might be what you were looking for.


-------
Signals
-------
A pre_update signal is sent when user data is about to be updated with new
values from authorization service provider, this apply to new users and already
existent ones. This is useful to update custom user fields or `User Profiles`_,
for example, to store user gender, location, etc. Example::

    from social_auth.signals import pre_update
    from social_auth.backends import FacebookBackend

    def facebook_extra_values(sender, user, response, details):
        user.gender = response.get('gender')
        return True

    pre_update.connect(facebook_extra_values, sender=FacebookBackend)

New data updating is made automatically but could be disabled and left only to
signal handler if this setting value::

    SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = False

is set to True.


------
OpenId
------
OpenId_ support is simpler to implement than OAuth_. Google and Yahoo
providers are supported by default, others are supported by POST method
providing endpoint URL.


-----
OAuth
-----
OAuth_ communication demands a set of keys exchange to validate the client
authenticity prior to user approbation. Twitter, Facebook and Orkut
facilitates these keys by application registration, Google works the same,
but provides the option for unregisterd applications.

Check next sections for details.


-------
Twitter
-------
Twitter offers per application keys named "Consumer Key" and
"Consumer Secret". To enable Twitter these two keys are needed.
Further documentation at `Twitter development resources`_:

- Register a new application at `Twitter App Creation`_,

- mark the "Yes, use Twitter for login" checkbox, and

- fill "Consumer Key" and "Consumer Secret" values::

      TWITTER_CONSUMER_KEY
      TWITTER_CONSUMER_SECRET

- You don't need to specify the URL callback


--------
Facebook
--------
Facebook works similar to Twitter but it's simpler to setup and
redirect URL is passed as a parameter when issuing an authorization.
Further documentation at `Facebook development resources`_:

- Register a new application at `Facebook App Creation`_, and

- fill "App Id" and "App Secret" values in values::

      FACEBOOK_APP_ID
      FACEBOOK_API_SECRET

- also it's possible to define extra permissions with::

     FACEBOOK_EXTENDED_PERMISSIONS = [...]


-----
Orkut
-----
Orkut offers per application keys named "Consumer Key" and
"Consumer Secret". To enable Orkut these two keys are needed.

Check `Google support`_ and `Orkut API`_ for details on getting
your consumer_key and consumer_secret keys.

- fill "Consumer Key" and "Consumer Secret" values::

      ORKUT_CONSUMER_KEY
      ORKUT_CONSUMER_SECRET

- add any needed extra data to::

      ORKUT_EXTRA_DATA = ''

- configure extra scopes in::

      ORKUT_EXTRA_SCOPES = [...]


------------
Google OAuth
------------
Google provides "Consumer Key" and "Consumer Secret" keys to
registered applications, but also allows unregistered application to
use their authorization system with, but beware that this method
will display a security banner to the user telling that the application
is not trusted.

Check `Google OAuth`_ and make your choice.

- fill "Consumer Key" and "Consumer Secret" values::

      GOOGLE_CONSUMER_KEY
      GOOGLE_CONSUMER_SECRET

anonymous values will be used if not configured as described in their
`OAuth reference`_


- configure the display name to be used in the "grant permissions" dialog
  that Google will display to users in::

      GOOGLE_DISPLAY_NAME = ''

  shows 'Social Auth' by default, but that might not suite your application.

- setup any needed extra scope in::

      GOOGLE_OAUTH_EXTRA_SCOPE = [...]

check which Apps are included in their `Google Data Protocol Directory`_


----
Bugs
----
Maybe several, please create `issues in github`_


------------
Contributors
------------
Attributions to whom deserves:

- caioariede_ (Caio Ariede):

  - Improvements and Orkut support

- krvss_ (Stas Kravets):

  - Initial setup.py configuration

- jezdez_ (Jannis Leidel):

  - Improvements and documentation update

- alfredo_ (Alfredo Ramirez)

  - Facebook and Doc improvements

- mattucf_ (Matt Brown)

  - Twitter and OAuth improvements



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

.. _Model Manager: http://docs.djangoproject.com/en/dev/topics/db/managers/#managers
.. _Login URL: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-url
.. _Login redirect URL: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-redirect-url
.. _AUTHENTICATION_BACKENDS: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#authentication-backends
.. _auth.User: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py#L186
.. _auth.UserManager: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py#L114
.. _login_required: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/decorators.py#L39
.. _User Profiles: http://www.djangobook.com/en/1.0/chapter12/#cn222
.. _OpenId: http://openid.net/
.. _OAuth: http://oauth.net/
.. _django-twitter-oauth: https://github.com/henriklied/django-twitter-oauth
.. _django-openid-auth: https://launchpad.net/django-openid-auth
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _python-oauth: https://github.com/leah/python-oauth
.. _Twitter development resources: http://dev.twitter.com/pages/auth
.. _Twitter App Creation: http://twitter.com/apps/new
.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/
.. _Google support: http://www.google.com/support/a/bin/answer.py?hl=en&answer=162105
.. _Orkut API:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _Google OpenID: http://code.google.com/apis/accounts/docs/OpenID.html
.. _Google OAuth: http://code.google.com/apis/accounts/docs/OAuth.html
.. _Google Data Protocol Directory: http://code.google.com/apis/gdata/docs/directory.html
.. _OAuth reference: http://code.google.com/apis/accounts/docs/OAuth_ref.html#SigningOAuth
.. _Yahoo OpenID: http://openid.yahoo.com/
.. _Twitter OAuth: http://dev.twitter.com/pages/oauth_faq
.. _Facebook OAuth: http://developers.facebook.com/docs/authentication/
.. _Orkut OAuth:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _myOpenID: https://www.myopenid.com/
.. _pypi: http://pypi.python.org/pypi/django-social-auth/
.. _github: https://github.com/omab/django-social-auth
.. _issues in github: https://github.com/omab/django-social-auth/issues
.. _caioariede: https://github.com/caioariede
.. _krvss: https://github.com/krvss
.. _jezdez: https://github.com/jezdez
.. _alfredo: https://github.com/alfredo
.. _mattucf: https://github.com/mattucf
.. _LiveJournal OpenID: http://www.livejournal.com/support/faqbrowse.bml?faqid=283
