==================
Django Social Auth
==================

Django Social Auth is an easy to setup social authentication/authorization
mechanism for Django projects.

Crafted using base code from django-twitter-oauth_ and django-openid-auth_,
implements a common interface to define new authentication providers from
third parties.

You can check this documentation on `Read the Docs`_ too.

----
Demo
----
There's a demo at http://social.matiasaguirre.net/.
Note: It lacks some backends support at the moment.


--------
Features
--------
This application provides user registration and login using social sites
credentials, some features are:

- Registration and Login using social sites using the following providers
  at the moment:

    * `Google OpenID`_
    * `Google OAuth`_
    * `Google OAuth2`_
    * `Yahoo OpenID`_
    * OpenId_ like myOpenID_
    * `Twitter OAuth`_
    * `Facebook OAuth`_

  Some contributions added support for:

    * `LiveJournal OpenID`_
    * `Orkut OAuth`_
    * `Linkedin OAuth`_
    * `Foursquare OAuth2`_
    * `GitHub OAuth`_
    * `Dropbox OAuth`_

- Basic user data population and signaling, to allows custom fields values
  from providers response

- Multiple social accounts association to single users

- Custom User model override if needed (`auth.User`_ by default)


------------
Dependencies
------------
Dependencies that **must** be meet to use the application:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on python-oauth2_

- Several backends demands application registration on their corresponding
  sites.


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
- Add social_auth to ``PYTHONPATH`` and installed applications::

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

- Add desired authentication backends to AUTHENTICATION_BACKENDS_ setting::

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.twitter.TwitterBackend',
        'social_auth.backends.facebook.FacebookBackend',
        'social_auth.backends.google.GoogleOAuthBackend',
        'social_auth.backends.google.GoogleOAuth2Backend',
        'social_auth.backends.google.GoogleBackend',
        'social_auth.backends.yahoo.YahooBackend',
        'social_auth.backends.contrib.linkedin.LinkedinBackend',
        'social_auth.backends.contrib.livejournal.LiveJournalBackend',
        'social_auth.backends.contrib.orkut.OrkutBackend',
        'social_auth.backends.contrib.foursquare.FoursquareBackend',
        'social_auth.backends.contrib.github.GithubBackend',
        'social_auth.backends.contrib.dropbox.DropboxBackend',
        'social_auth.backends.OpenIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

- The application will try to import custom backends from the sources defined in::

    SOCIAL_AUTH_IMPORT_BACKENDS = (
        'myproy.social_auth_extra_services',
    )

  This way it's easier to add new providers, check the already defined ones
  in ``social_auth.backends`` for examples.

  Take into account that backends **must** be defined in AUTHENTICATION_BACKENDS_
  or Django won't pick them when trying to authenticate the user.

- Define desired backends for your site::

    SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'google-oauth', 'facebook', ...)

  All backends are enabled by default.

- Setup needed OAuth keys (see OAuth_ section for details)::

    TWITTER_CONSUMER_KEY         = ''
    TWITTER_CONSUMER_SECRET      = ''
    FACEBOOK_APP_ID              = ''
    FACEBOOK_API_SECRET          = ''
    LINKEDIN_CONSUMER_KEY        = ''
    LINKEDIN_CONSUMER_SECRET     = ''
    ORKUT_CONSUMER_KEY           = ''
    ORKUT_CONSUMER_SECRET        = ''
    GOOGLE_CONSUMER_KEY          = ''
    GOOGLE_CONSUMER_SECRET       = ''
    GOOGLE_OAUTH2_CLIENT_ID      = ''
    GOOGLE_OAUTH2_CLIENT_SECRET  = ''
    FOURSQUARE_CONSUMER_KEY      = ''
    FOURSQUARE_CONSUMER_SECRET   = ''
    GITHUB_APP_ID                = ''
    GITHUB_API_SECRET            = ''
    DROPBOX_APP_ID               = ''
    DROPBOX_API_SECRET           = ''

- Setup login URLs::

    LOGIN_URL          = '/login-form/'
    LOGIN_REDIRECT_URL = '/logged-in/'
    LOGIN_ERROR_URL    = '/login-error/'

  Check Django documentation at `Login URL`_ and `Login redirect URL`_

  If a custom redirect URL is needed that must be different to ``LOGIN_URL``,
  define the setting::

    SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/another-login-url/'

  A different URL could be defined for newly registered users::

    SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'

  or for newly associated accounts::

    SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'

  or for account disconnections::

    SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'

  In case of authentication error, the message can be stored in session
  if the following setting is defined::

    SOCIAL_AUTH_ERROR_KEY = 'social_errors'

  This defines the desired session key where last error message should be
  stored. It's disabled by default.

- Configure authentication and association complete URL names to avoid
  possible clashes::

    SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
    SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

- Add URLs entries::

    urlpatterns = patterns('',
        ...
        url(r'', include('social_auth.urls')),
        ...
    )

  All ``django-social-auth`` URLs names have ``socialauth_`` prefix.

- Define context processors if needed::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'social_auth.context_processors.social_auth_by_type_backends',
    )

   check `social_auth.context_processors`.

- Sync database to create needed models::

    ./manage.py syncdb

- Not mandatory, but recommended::

    SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

  or::

    import random
    SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])

  or::

    from django.template.defaultfilters import slugify
    SOCIAL_AUTH_USERNAME_FIXER = lambda u: slugify(u)

  in case your user layout needs to purify username on some weird way.

  Final user name will have a random UUID-generated suffix in case it's already
  taken. The UUID token max length can be changed with the setting::

    SOCIAL_AUTH_UUID_LENGTH = 16

- Backends will store extra values from response by default, set this to False
  to avoid such behavior::

    SOCIAL_AUTH_EXTRA_DATA = False

  Also more extra values will be stored if defined, details about this setting
  are listed below on OpenId and OAuth sections.

  Session expiration time is an special value, it's recommended to define::

    SOCIAL_AUTH_EXPIRATION = 'expires'

  and use such setting name where expiration times are returned. View that
  completes login process will set session expiration time using this name if
  it's present or ``expires`` by default. Expiration configuration can be disabled
  with setting::

    SOCIAL_AUTH_SESSION_EXPIRATION = False

- It's possible to override the used ``User`` model if needed::

    SOCIAL_AUTH_USER_MODEL = 'myapp.CustomUser'

  This class **must** have a custom `Model Manager`_ with a ``create_user`` method
  that resembles the one on `auth.UserManager`_.

  Also, it's highly recommended that this class define the following fields::

    username   = CharField(...)
    last_login = DateTimeField(blank=True)
    is_active  = BooleanField(...)

  and the method::

    is_authenticated():
        ...

  These are needed to ensure a better ``django-auth`` integration, in other case
  `login_required`_ won't be usable. A warning is displayed if any of these are
  missing. By default `auth.User`_ is used.

  Check example application for implementation details, but first, please take
  a look to `User Profiles`_, it might be what you were looking for.

  It's possible to disable user creations by ``django-social-auth`` with::

      SOCIAL_AUTH_CREATE_USERS = False

  It is also possible to associate multiple user accounts with a single email
  address as long as the rest of the user data is unique. Set value as True 
  to enable, otherwise set as False to disable.
  This behavior is disabled by default (false) unless specifically set::

      SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

- You can send extra parameters on auth process by defining settings per
  provider, example to request Facebook to show Mobile authorization page,
  define::

      FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'touch'}

  For other providers, just define settings in the form::

      <uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}

- By default the application doesn't make redirects to different domains, to
  disable this behavior::

      SOCIAL_AUTH_SANITIZE_REDIRECTS = False


-------
Signals
-------
A ``pre_update`` signal is sent when user data is about to be updated with new
values from authorization service provider, this apply to new users and already
existent ones. This is useful to update custom user fields or `User Profiles`_,
for example, to store user gender, location, etc. Example::

    from social_auth.signals import pre_update
    from social_auth.backends.facebook import FacebookBackend

    def facebook_extra_values(sender, user, response, details, **kwargs):
        user.gender = response.get('gender')
        return True

    pre_update.connect(facebook_extra_values, sender=FacebookBackend)

New data updating is made automatically but could be disabled and left only to
signal handler if this setting value is set to True::

    SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = False

Take into account that when defining a custom ``User`` model and declaring signal
handler in ``models.py``, the imports and handler definition **must** be made
after the custom ``User`` model is defined or circular imports issues will be
raised.

Also a new-user signal (``socialauth_registered``) is sent when new accounts are
created::

    from social_auth.signals import socialauth_registered 

    def new_users_handler(sender, user, response, details, **kwargs):
        user.is_new = True
        return False

    socialauth_registered.connect(new_users_handler, sender=None)


------
OpenId
------
OpenId_ support is simpler to implement than OAuth_. Google and Yahoo
providers are supported by default, others are supported by POST method
providing endpoint URL.

OpenId_ backends can store extra data in ``UserSocialAuth.extra_data`` field
by defining a set of values names to retrieve from any of the used schemas,
``AttributeExchange`` and ``SimpleRegistration``. As their keywords differ we
need two settings.

Settings is per backend, so we have two possible values for each one. Name
is dynamically checked using uppercase backend name as prefix::

    <uppercase backend name>_SREG_EXTRA_DATA
    <uppercase backend name>_AX_EXTRA_DATA

Example::

    GOOGLE_SREG_EXTRA_DATA = [(..., ...)]
    GOOGLE_AX_EXTRA_DATA = [(..., ...)]

Settings must be a list of tuples mapping value name in response and value
alias used to store.


-----
OAuth
-----
OAuth_ communication demands a set of keys exchange to validate the client
authenticity prior to user approbation. Twitter, Facebook and Orkut
facilitates these keys by application registration, Google works the same,
but provides the option for unregistered applications.

Check next sections for details.

OAuth_ backends also can store extra data in ``UserSocialAuth.extra_data``
field by defining a set of values names to retrieve from service response.

Settings is per backend and it's name is dynamically checked using uppercase
backend name as prefix::

    <uppercase backend name>_EXTRA_DATA

Example::

    FACEBOOK_EXTRA_DATA = [(..., ...)]

Settings must be a list of tuples mapping value name in response and value
alias used to store.


-------
Twitter
-------
Twitter offers per application keys named ``Consumer Key`` and ``Consumer Secret``.
To enable Twitter these two keys are needed. Further documentation at
`Twitter development resources`_:

- Register a new application at `Twitter App Creation`_,

- mark the "Yes, use Twitter for login" checkbox, and

- fill ``Consumer Key`` and ``Consumer Secret`` values::

      TWITTER_CONSUMER_KEY
      TWITTER_CONSUMER_SECRET

- You need to specify an URL callback or the application will be marked as
  Client type instead of the Browser. Almost any dummy value will work if
  you plan some test.


--------
Facebook
--------
Facebook works similar to Twitter but it's simpler to setup and redirect URL
is passed as a parameter when issuing an authorization. Further documentation
at `Facebook development resources`_:

- Register a new application at `Facebook App Creation`_, and

- fill ``App Id`` and ``App Secret`` values in values::

      FACEBOOK_APP_ID
      FACEBOOK_API_SECRET

- also it's possible to define extra permissions with::

     FACEBOOK_EXTENDED_PERMISSIONS = [...]

If you define a redirect URL in Facebook setup page, be sure to not define
http://127.0.0.1:8000 or http://localhost:8000 because it won't work when
testing. Instead I define http://myapp.com and setup a mapping on /etc/hosts
or use dnsmasq_.


-----
Orkut
-----
Orkut offers per application keys named ``Consumer Key`` and ``Consumer Secret``.
To enable Orkut these two keys are needed.

Check `Google support`_ and `Orkut API`_ for details on getting
your consumer_key and consumer_secret keys.

- fill ``Consumer Key`` and ``Consumer Secret`` values::

      ORKUT_CONSUMER_KEY
      ORKUT_CONSUMER_SECRET

- add any needed extra data to::

      ORKUT_EXTRA_DATA = ''

- configure extra scopes in::

      ORKUT_EXTRA_SCOPES = [...]


------------
Google OAuth
------------
Google provides ``Consumer Key`` and ``Consumer Secret`` keys to registered
applications, but also allows unregistered application to use their authorization
system with, but beware that this method will display a security banner to the
user telling that the application is not trusted.

Check `Google OAuth`_ and make your choice.

- fill ``Consumer Key`` and ``Consumer Secret`` values::

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

Check which applications can be included in their `Google Data Protocol Directory`_


-------------
Google OAuth2
-------------
Recently Google launched OAuth2 support following the definition at `OAuth2 draft`.
It works in a similar way to plain OAuth mechanism, but developers **must** register
an application and apply for a set of keys. Check `Google OAuth2`_ document for details.

**Note**:
  This support is experimental as Google implementation may change and OAuth2 is still
  a draft.

To enable OAuth2 support:

- fill ``Client ID`` and ``Client Secret`` settings, these values can be obtained
  easily as described on `OAuth2 Registering`_ doc::

      GOOGLE_OAUTH2_CLIENT_ID = ''
      GOOGLE_OAUTH2_CLIENT_SECRET = ''

  previous name ``GOOGLE_OAUTH2_CLIENT_KEY`` is supported for backward
  compatibility.

- scopes are shared between OAuth mechanisms::

      GOOGLE_OAUTH_EXTRA_SCOPE = [...]

Check which applications can be included in their `Google Data Protocol Directory`_


--------
LinkedIn
--------
LinkedIn setup is similar to any other OAuth service. To request extra fields
using `LinkedIn fields selectors`_ just define the setting::

    LINKEDIN_EXTRA_FIELD_SELECTORS = [...]

with the needed fields selectors, also define LINKEDIN_EXTRA_DATA properly, that
way the values will be stored in ``UserSocialAuth.extra_data`` field.

By default ``id``, ``first-name`` and ``last-name`` are requested and stored.


------
GitHub
------
GitHub works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, and

- fill ``App Id`` and ``App Secret`` values in the settings::

      GITHUB_APP_ID = ''
      GITHUB_API_SECRET = ''

- also it's possible to define extra permissions with::

     GITHUB_EXTENDED_PERMISSIONS = [...]
 

-------
Dropbox
-------
Dropbox uses OAuth v1.0 for authentication.

- Register a new application at `Dropbox Developers`_, and

- fill ``App Key`` and ``App Secret`` values in the settings::

      DROPBOX_APP_ID = ''
      DROPBOX_API_SECRET = ''

-------
Testing
-------
To test the app just run::

    ./manage.py test social_auth

This will run a bunch of tests, so far only login process is tested, more
will come eventually.

User accounts on the different sites are needed to run tests, configure the
credentials in the following way::

    # twitter testing
    TEST_TWITTER_USER = 'testing_account'
    TEST_TWITTER_PASSWORD = 'password_for_testing_account'

    # facebook testing
    TEST_FACEBOOK_USER = 'testing_account'
    TEST_FACEBOOK_PASSWORD = 'password_for_testing_account'

    # google testing
    TEST_GOOGLE_USER = 'testing_account@gmail.com'
    TEST_GOOGLE_PASSWORD = 'password_for_testing_account'


There's support for Selenium_ tests too on root contrib directory. To run
install selenium::

    $ pip install selenium

and create a ``test_settings.py`` copying ``test_settings.py.template`` and
fill the needed account information. Then run::

    cd contrib/tests
    ./runtests.py


-------------
Miscellaneous
-------------

Join to django-social-auth_ community on Convore_ and bring any questions or
suggestions that will improve this app.


South_ users should add this rule to enable migrations::

    try:
        import south
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], ["^social_auth\.fields\.JSONField"])
    except:
        pass


If defining a custom user model, do not import social_auth from any models.py
that would finally import from the models.py that defines your User class or it
will make your project fail with a recursive import because social_auth uses
get_model() to retrieve your User.


There's an ongoing movement to create a list of third party backends on
djangopackages.com_, so, if somebody doesn't want it's backend in the
``contrib`` directory but still wants to share, just split it in a separated
package and link it there.


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

- Quard_ (Vadym Zakovinko)

  - LinkedIn support

- micrypt_ (Seyi Ogunyemi)

  - OAuth2 migration

- bedspax_

  - Foursquare support

- revolunet_ (Julien Bouquillon)

  - GitHub support

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
.. _python-oauth2: https://github.com/simplegeo/python-oauth2
.. _Twitter development resources: http://dev.twitter.com/pages/auth
.. _Twitter App Creation: http://twitter.com/apps/new
.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/
.. _Google support: http://www.google.com/support/a/bin/answer.py?hl=en&answer=162105
.. _Orkut API:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _Google OpenID: http://code.google.com/apis/accounts/docs/OpenID.html
.. _Google OAuth: http://code.google.com/apis/accounts/docs/OAuth.html
.. _Google OAuth2: http://code.google.com/apis/accounts/docs/OAuth2.html
.. _OAuth2 Registering: http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
.. _Google Data Protocol Directory: http://code.google.com/apis/gdata/docs/directory.html
.. _OAuth2 draft: http://tools.ietf.org/html/draft-ietf-oauth-v2-10
.. _OAuth reference: http://code.google.com/apis/accounts/docs/OAuth_ref.html#SigningOAuth
.. _Yahoo OpenID: http://openid.yahoo.com/
.. _Twitter OAuth: http://dev.twitter.com/pages/oauth_faq
.. _Facebook OAuth: http://developers.facebook.com/docs/authentication/
.. _Linkedin OAuth: https://www.linkedin.com/secure/developer
.. _Orkut OAuth:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _myOpenID: https://www.myopenid.com/
.. _LiveJournal OpenID: http://www.livejournal.com/support/faqbrowse.bml?faqid=283
.. _Foursquare OAuth2: https://developer.foursquare.com/docs/oauth.html
.. _pypi: http://pypi.python.org/pypi/django-social-auth/
.. _github: https://github.com/omab/django-social-auth
.. _issues in github: https://github.com/omab/django-social-auth/issues
.. _caioariede: https://github.com/caioariede
.. _krvss: https://github.com/krvss
.. _jezdez: https://github.com/jezdez
.. _alfredo: https://github.com/alfredo
.. _mattucf: https://github.com/mattucf
.. _Quard: https://github.com/Quard
.. _micrypt: https://github.com/micrypt
.. _South: http://south.aeracode.org/
.. _bedspax: https://github.com/bedspax
.. _django-social-auth: https://convore.com/django-social-auth/
.. _Convore: https://convore.com/
.. _Selenium: http://seleniumhq.org/
.. _LinkedIn fields selectors: http://developer.linkedin.com/docs/DOC-1014
.. _Read the Docs: http://django-social-auth.readthedocs.org/
.. _revolunet: https://github.com/revolunet
.. _GitHub OAuth: http://developer.github.com/v3/oauth/
.. _GitHub Developers: https://github.com/account/applications/new
.. _djangopackages.com: http://djangopackages.com/grids/g/social-auth-backends/
.. _Dropbox OAuth: https://www.dropbox.com/developers_beta/reference/api
.. _Dropbox Developers: https://www.dropbox.com/developers/apps
