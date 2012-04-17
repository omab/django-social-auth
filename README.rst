Django Social Auth
==================

Django Social Auth is an easy to setup social authentication/authorization
mechanism for Django projects.

Crafted using base code from django-twitter-oauth_ and django-openid-auth_,
implements a common interface to define new authentication providers from
third parties.

You can check this documentation on `Read the Docs`_ too.

.. contents:: Table of Contents

Demo
----

There's a demo at http://social.matiasaguirre.net/.
Note: It lacks some backends support at the moment.

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
    * `Flickr OAuth`_
    * `Vkontakte OAuth`_

- Basic user data population and signaling, to allows custom fields values
  from providers response

- Multiple social accounts association to single users

- Custom User model override if needed (`auth.User`_ by default)

- Extensible pipeline to handle authentication/association mechanism

Dependencies
------------

Dependencies that **must** be meet to use the application:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on python-oauth2_

- Several backends demands application registration on their corresponding
  sites.

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

Configuration
-------------

- Add social_auth to ``PYTHONPATH`` and installed applications::

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

- Add desired authentication backends to Django's AUTHENTICATION_BACKENDS_ setting::

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.twitter.TwitterBackend',
        'social_auth.backends.facebook.FacebookBackend',
        'social_auth.backends.google.GoogleOAuthBackend',
        'social_auth.backends.google.GoogleOAuth2Backend',
        'social_auth.backends.google.GoogleBackend',
        'social_auth.backends.yahoo.YahooBackend',
        'social_auth.backends.browserid.BrowserIDBackend',
        'social_auth.backends.contrib.linkedin.LinkedinBackend',
        'social_auth.backends.contrib.livejournal.LiveJournalBackend',
        'social_auth.backends.contrib.orkut.OrkutBackend',
        'social_auth.backends.contrib.foursquare.FoursquareBackend',
        'social_auth.backends.contrib.github.GithubBackend',
        'social_auth.backends.contrib.dropbox.DropboxBackend',
        'social_auth.backends.contrib.flickr.FlickrBackend',
        'social_auth.backends.contrib.instagram.InstagramBackend',
        'social_auth.backends.contrib.vkontakte.VkontakteBackend',
        'social_auth.backends.OpenIDBackend',
        'social_auth.backends.contrib.bitbucket.BitbucketBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

  Take into account that backends **must** be defined in AUTHENTICATION_BACKENDS_
  or Django won't pick them when trying to authenticate the user.

  Don't miss ``django.contrib.auth.backends.ModelBackend`` if using ``django.auth``
  user model or users won't be able to login.

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
    FLICKR_APP_ID                = ''
    FLICKR_API_SECRET            = ''
    INSTAGRAM_CLIENT_ID          = ''
    INSTAGRAM_CLIENT_SECRET      = ''
    VK_APP_ID                    = ''
    VK_API_SECRET                = ''
    BITBUCKET_CONSUMER_KEY       = ''
    BITBUCKET_CONSUMER_SECRET    = ''

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

  Users will be redirected to ``LOGIN_ERROR_URL`` in case of error or user
  cancellation on some backends. This URL can be override by this setting::

    SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'

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
        'social_auth.context_processors.social_auth_by_name_backends',
        'social_auth.context_processors.social_auth_backends',
        'social_auth.context_processors.social_auth_by_type_backends',
    )

  * ``social_auth_by_name_backends``:
    Adds a ``social_auth`` dict where each key is a provider name and its value
    is a UserSocialAuth instance if user has associated an account with that
    provider, otherwise ``None``.

  * ``social_auth_backends``:
    Adds a ``social_auth`` dict with keys are ``associated``, ``not_associated`` and
    ``backends``. ``associated`` key is a list of ``UserSocialAuth`` instances
    associated with current user. ``not_associated`` is a list of providers names
    that the current user doesn't have any association yet. ``backends`` holds
    the list of backend names supported.

  * ``social_auth_by_type_backends``:
    Simiar to ``social_auth_backends`` but each value is grouped by backend type
    ``openid``, ``oauth2`` and ``oauth``.

  Check ``social_auth.context_processors`` for details.

  **Note**:
  ``social_auth_backends`` and ``social_auth_by_type_backends`` don't play nice
  together.

- Sync database to create needed models::

    ./manage.py syncdb

- Not mandatory, but recommended::

    SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

  or::

    import random
    SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])

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
  address, set value as True to enable, otherwise set as False to disable.
  This behavior is enabled by default (True) unless specifically set::

      SOCIAL_AUTH_ASSOCIATE_BY_MAIL = False

- You can send extra parameters on auth process by defining settings per
  provider, example to request Facebook to show Mobile authorization page,
  define::

      FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'touch'}

  For other providers, just define settings in the form::

      <uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}

- Also, you can send extra parameters on request token process by defining
  settings per provider in the same way explained above but with this other
  suffix::

      <uppercase backend name>_REQUEST_TOKEN_EXTRA_ARGUMENTS = {...}

- By default the application doesn't make redirects to different domains, to
  disable this behavior::

      SOCIAL_AUTH_SANITIZE_REDIRECTS = False

- Inactive users can be redirected to a different page if this setting is
  defined::

      SOCIAL_AUTH_INACTIVE_USER_URL = '...'

  Defaults to ``LOGIN_ERROR_URL``.

- The application catches any exception and logs errors to ``logger`` or
  ``django.contrib.messagess`` application by default. But it's possible to
  override the default behavior by defining a function to process the
  exceptions using this setting::

    SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.process_exceptions'

  The function parameters will ``request`` holding the current request object,
  ``backend`` with the current backend and ``err`` which is the exception
  instance.

  Recently this set of exceptions were introduce to describe the situations
  a bit more than the old ``ValueError`` usually raised::

    AuthException           - Base exception class
    AuthFailed              - Authentication failed for some reason
    AuthCanceled            - Authentication was canceled by the user
    AuthUnknownError        - An unknown error stoped the authentication
                              process
    AuthTokenError          - Unauthorized or access token error, it was
                              invalid, impossible to authenticate or user
                              removed permissions to it.
    AuthMissingParameter    - A needed parameter to continue the process was
                              missing, usually raised by the services that
                              need some POST data like myOpenID

  These are a subclass of ``ValueError`` to keep backward compatibility.

  Having tracebacks is really useful when debugging, for that purpose this
  setting was defined::

    SOCIAL_AUTH_RAISE_EXCEPTIONS = DEBUG

  It's default value is ``DEBUG``, so you need to set it to ``False`` to avoid
  tracebacks when ``DEBUG = True``.

- When your project is behind a reverse proxy that uses HTTPS the redirect URIs
  can became with the wrong schema (``http://`` instead of ``https://``), and
  might cause errors with the auth process, to force HTTPS in the final URIs
  define this setting::

    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


Some settings can be tweak by backend by adding the backend name prefix (all
uppercase and replace ``-`` with ``_``), here's the supported settings so far::

        LOGIN_ERROR_URL
        SOCIAL_AUTH_BACKEND_ERROR_URL
        SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL
        SOCIAL_AUTH_DISCONNECT_REDIRECT_URL
        SOCIAL_AUTH_NEW_USER_REDIRECT_URL
        SOCIAL_AUTH_LOGIN_REDIRECT_URL
        SOCIAL_AUTH_INACTIVE_USER_URL


Authentication Pipeline
-----------------------

The final process of the authentication workflow is handled by a operations
pipeline where custom functions can be added or default items can be removed to
provide a custom behavior.

The default pipeline mimics the user creation and basic data gathering from
previous django-social-auth_ versions and a big set of settings (listed below)
that were used to alter the default behavior are now deprecated in favor of
pipeline overrides.

The default pipeline is composed by::

    (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.associate.associate_by_email',
        'social_auth.backends.pipeline.user.get_username',
        'social_auth.backends.pipeline.user.create_user',
        'social_auth.backends.pipeline.social.associate_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

But it's possible to override it by defining the setting
``SOCIAL_AUTH_PIPELINE``, for example a pipeline that won't create users, just
accept already registered ones would look like this::

    SOCIAL_AUTH_PIPELINE = (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

Each pipeline function will receive the following parameters:
    * Current social authentication backend
    * User ID given by authentication provider
    * User details given by authentication provider
    * ``is_new`` flag (initialized in ``False``)
    * Any arguments passed to ``auth_complete`` backend method, default views
      pass this arguments:

      - current logged in user (if it's logged in, otherwise ``None``)
      - current request

Each pipeline entry must return a ``dict`` or ``None``, any value in the
``dict`` will be used in the ``kwargs`` argument for the next pipeline entry.

The workflow will be cut if the exception ``social_auth.backends.exceptions.StopPipeline``
is raised at any point.

If any function returns something else beside a ``dict`` or ``None``, the
workflow will be cut and the value returned immediately, this is useful to
return ``HttpReponse`` instances like ``HttpResponseRedirect``.

Partial Pipeline
----------------

It's possible to cut the pipeline process to return to the user asking for more
data and resume the process later, to accomplish this add the entry
``social_auth.backends.pipeline.misc.save_status_to_session`` (or a similar
implementation) to the pipeline setting before any entry that returns an
``HttpResponse`` instance::

    SOCIAL_AUTH_PIPELINE = (
        ...
        social_auth.backends.pipeline.misc.save_status_to_session,
        app.pipeline.redirect_to_basic_user_data_form
        ...
    )

When it's time to resume the process just redirect the user to
``/complete/<backend>/`` view. By default the pipeline will be resumed in the
next entry after ``save_status_to_session`` but this can be modified by setting
the following setting to the import path of the pipeline entry to resume
processing::

    SOCIAL_AUTH_PIPELINE_RESUME_ENTRY = 'social_auth.backends.pipeline.misc.save_status_to_session'

``save_status_to_session`` saves needed data into user session, the key can be
defined by ``SOCIAL_AUTH_PARTIAL_PIPELINE_KEY`` which default value is
``partial_pipeline``::

    SOCIAL_AUTH_PARTIAL_PIPELINE_KEY = 'partial_pipeline'

Check the `example application`_ to check a basic usage.

Deprecated bits
---------------

The following settings are deprecated in favor of pipeline functions.

- These settings should be avoided and override ``get_username`` pipeline entry
  with the desired behavior::

    SOCIAL_AUTH_FORCE_RANDOM_USERNAME
    SOCIAL_AUTH_DEFAULT_USERNAME
    SOCIAL_AUTH_UUID_LENGTH
    SOCIAL_AUTH_USERNAME_FIXER

- User creation setting should be avoided and remove the entry ``create_user``
  from pipeline instead::

    SOCIAL_AUTH_CREATE_USERS

- Automatic data update should be stopped by overriding ``update_user_details``
  pipeline entry instead of using this setting::

    SOCIAL_AUTH_CHANGE_SIGNAL_ONLY

- Extra data retrieval from providers should be stopped by removing
  ``load_extra_data`` from pipeline instead of using this setting::

    SOCIAL_AUTH_EXTRA_DATA

- Automatic email association should be avoided by removing
  ``associate_by_email`` pipeline entry instead of using this setting::

    SOCIAL_AUTH_ASSOCIATE_BY_MAIL

Usage example
-------------

Authentication process starts with ``socialauth_begin`` URL.

Template code example::

    <ul>
      <li>
        <a href="{% url socialauth_begin 'twitter' %}">Enter using Twitter</a>
      </li>
      <li>
        <a href="{% url socialauth_begin 'facebook' %}">Enter using Facebook</a>
      </li>
    </ul>

In the example above we assume that Twitter and Facebook authentication backends enabled, and following settings provided::

    TWITTER_CONSUMER_KEY = 'real key here'
    TWITTER_CONSUMER_SECRET = 'real secret here'
    FACEBOOK_APP_ID = 'real id here'
    FACEBOOK_API_SECRET = 'real secret here'

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


Tokens
------

Almost every service covered provide some kind of API that is protected with
``access_token`` or token pairs (like `Twitter OAuth keys`_). These tokens are
gathered by the authentication mechanism and stored in
``UserSocialAuth.extra_data``.

``UserSocialAuth`` has a property named ``tokens`` to easilly access this
useful values, it will return a dictionary containing the tokens values.
A simple usage example::

    >>> from pprint import pprint
    >>> from social_auth.models import UserSocialAuth
    >>> instance = UserSocialAuth.objects.filter(provider='twitter').get(...)
    >>> pprint(instance.tokens)
    {u'oauth_token': u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
     u'oauth_token_secret': u'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'}
    >>> instance = UserSocialAuth.objects.filter(provider='facebook').get(...)
    >>> pprint(instance.tokens)
    {u'access_token': u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}


Backends
--------

OpenId
^^^^^^

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
alias used to store. A third value (boolean) is supported to, it's purpose is
to signal if the value should be discarded if it evaluates to ``False``, this
is to avoid replacing old (needed) values when they don't form part of current
response. If not present, then this check is avoided and the value will replace
any data.

OAuth
^^^^^

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
alias used to store. A third value (boolean) is supported to, it's purpose is
to signal if the value should be discarded if it evaluates to ``False``, this
is to avoid replacing old (needed) values when they don't form part of current
response. If not present, then this check is avoided and the value will replace
any data.


Twitter
^^^^^^^

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

Facebook
^^^^^^^^

Facebook works similar to Twitter but it's simpler to setup and redirect URL
is passed as a parameter when issuing an authorization. Further documentation
at `Facebook development resources`_:

- Register a new application at `Facebook App Creation`_, and

- fill ``App Id`` and ``App Secret`` values in values::

      FACEBOOK_APP_ID
      FACEBOOK_API_SECRET

- Define ``FACEBOOK_EXTENDED_PERMISSIONS`` to get extra permissions from facebook.
  NOTE: to get users' email addresses, you must request the 'email' permission::

     FACEBOOK_EXTENDED_PERMISSIONS = ['email']


  Take into account that Facebook doesn't return user email by default, this
  setting is needed if email is required::

     FACEBOOK_EXTENDED_PERMISSIONS = ['email']

- Define ``FACEBOOK_PROFILE_EXTRA_PARAMS`` to pass extra parameters to
  https://graph.facebook.com/me when gathering the user profile data, like::

    FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

If you define a redirect URL in Facebook setup page, be sure to not define
http://127.0.0.1:8000 or http://localhost:8000 because it won't work when
testing. Instead I define http://myapp.com and setup a mapping on /etc/hosts
or use dnsmasq_.

Orkut
^^^^^

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

Google OAuth
^^^^^^^^^^^^

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

Google OAuth2
^^^^^^^^^^^^^

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

LinkedIn
^^^^^^^^

LinkedIn setup is similar to any other OAuth service. To request extra fields
using `LinkedIn fields selectors`_ just define the setting::

    LINKEDIN_EXTRA_FIELD_SELECTORS = [...]

with the needed fields selectors, also define LINKEDIN_EXTRA_DATA properly, that
way the values will be stored in ``UserSocialAuth.extra_data`` field.

By default ``id``, ``first-name`` and ``last-name`` are requested and stored.

GitHub
^^^^^^

GitHub works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, set your site domain as
  the callback URL or it might cause some troubles when associating accounts,

- Fill ``App Id`` and ``App Secret`` values in the settings::

      GITHUB_APP_ID = ''
      GITHUB_API_SECRET = ''

- Also it's possible to define extra permissions with::

     GITHUB_EXTENDED_PERMISSIONS = [...]
     
Bitbucket
^^^^^^^^^

Bitbucket works similar to Twitter (OAuth).

- Register a new application by emailing ``support@bitbucket.org`` with an
  application name and a bit of a description,

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      BITBUCKET_CONSUMER_KEY = ''
      BITBUCKET_CONSUMER_SECRET = ''

Dropbox
^^^^^^^

Dropbox uses OAuth v1.0 for authentication.

- Register a new application at `Dropbox Developers`_, and

- fill ``App Key`` and ``App Secret`` values in the settings::

      DROPBOX_APP_ID = ''
      DROPBOX_API_SECRET = ''

Flickr
^^^^^^

Flickr uses OAuth v1.0 for authentication.

- Register a new application at the `Flickr App Garden`_, and

- fill ``Key`` and ``Secret`` values in the settings::

      FLICKR_APP_ID = ''
      FLICKR_API_SECRET = ''

BrowserID
^^^^^^^^^

Support for BrowserID_ is possible by posting the ``assertion`` code to
``/complete/browserid/`` URL.

The setup doesn't need any setting, just the usual BrowserID_ javascript
include in your document and the needed mechanism to trigger the POST to
`django-social-auth`_.

Check the second "Use Case" for an implementation example.

Instagram
^^^^^^^^^

Instagram uses OAuth v2 for Authentication

- Register a new application at the `Instagram API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      INSTAGRAM_CLIENT_ID = ''
      INSTAGRAM_CLIENT_SECRET = ''

.. note::

    Instagram only allows one callback url so you'll have to change your urls.py to
    accomodate both ``/complete`` and ``/associate`` routes, for example by having
    a single ``/associate`` url which takes a ``?complete=true`` parameter for the
    cases when you want to complete rather than associate.

Vkontakte
^^^^^^^^^

Vkontakte uses OAuth v2 for Authentication

- Register a new application at the `Vkontakte API`_, and

- fill ``App Id`` and ``Api Secret`` values in the settings::

      VK_APP_ID = ''
      VK_API_SECRET = ''

- Also it's possible to define extra permissions with::

     VK_EXTRA_SCOPE = [...]

  See the `names of the privileges VKontakte`_.

Testing
-------

To test the application just run::

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

Use Cases
---------
Some particular use cases are listed below.

1. Use social auth just for account association (no login)::

    urlpatterns += patterns('',
        url(r'^associate/(?P<backend>[^/]+)/$', associate,
            name='socialauth_associate_begin'),
        url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
            name='socialauth_associate_complete'),
        url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect,
            name='socialauth_disconnect'),
        url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
            disconnect, name='socialauth_disconnect_individual'),
    )

2. Include a similar snippet in your page to make BrowserID_ work::

    <!-- Include BrowserID JavaScript -->
    <script src="https://browserid.org/include.js" type="text/javascript"></script>

    <!-- Define a form to send the POST data -->
    <form method="post" action="{% url socialauth_complete "browserid" %}">
        <input type="hidden" name="assertion" value="" />
        <a rel="nofollow" id="browserid" href="#">BrowserID</a>
    </form>

    <!-- Setup click handler that retieves BrowserID assertion code and sends
         POST data -->
    <script type="text/javascript">
        $(function () {
            $('#browserid').click(function (e) {
                e.preventDefault();
                var self = $(this);

                navigator.id.get(function (assertion) {
                    if (assertion) {
                        self.parent('form')
                                .find('input[type=hidden]')
                                    .attr('value', assertion)
                                    .end()
                                .submit();
                    } else {
                        alert('Some error occurred');
                    }
                });
            });
        });
    </script>

Miscellaneous
-------------

Mailing list
^^^^^^^^^^^^
Join to `django-social-auth discussion list`_ and bring any questions or suggestions
that would improve this application. Convore_ discussion group is deprecated since
the service is going to be shut down on April 1st.

South users
^^^^^^^^^^^
South_ users should add this rule to enable migrations::

    try:
        import south
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], ["^social_auth\.fields\.JSONField"])
    except:
        pass

Custom User model
^^^^^^^^^^^^^^^^^
If defining a custom user model, do not import ``social_auth`` from any
``models.py`` that would finally import from the ``models.py`` that defines
your ``User`` class or it will make your project fail with a recursive import
because ``social_auth`` uses ``get_model()`` to retrieve your User.

Third party backends
^^^^^^^^^^^^^^^^^^^^
There's an ongoing movement to create a list of third party backends on
djangopackages.com_, so, if somebody doesn't want it's backend in the
``contrib`` directory but still wants to share, just split it in a separated
package and link it there.

Python 2.7.2rev4, 2.7.3 and Facebook backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Seems that this bug described in StackOverflow_ hits users using
django-social-auth_ with Python versions 2.7.2rev4 and 2.7.3 (so far) and
Facebook backend. The bug report `#315`_ explains it a bit more and shows
a workaround fit avoid it.

Bugs
----

Maybe several, please create `issues in github`_

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

- danielgtaylor_ (Daniel G. Taylor)

  - Dropbox support
  - Flickr support
  - Provider name context processor

- r4vi_ (Ravi Kotecha)

  - Instagram support

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
.. _r4vi: https://github.com/r4vi
.. _South: http://south.aeracode.org/
.. _bedspax: https://github.com/bedspax
.. _django-social-auth: https://github.com/omab/django-social-auth
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
.. _Flickr OAuth: http://www.flickr.com/services/api/
.. _Flickr App Garden: http://www.flickr.com/services/apps/create/
.. _danielgtaylor: https://github.com/danielgtaylor
.. _example application: https://github.com/omab/django-social-auth/blob/master/example/local_settings.py.template#L23
.. _BrowserID: https://browserid.org
.. _Instagram API: http://instagr.am/developer/
.. _django-social-auth discussion list: https://groups.google.com/group/django-social-auth
.. _Twitter OAuth keys: https://dev.twitter.com/docs/auth/authorizing-request
.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
.. _names of the privileges VKontakte: http://vk.com/developers.php?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
.. _Vkontakte API: http://vk.com/developers.php
.. _StackOverflow: http://stackoverflow.com/questions/9835506/urllib-urlopen-works-on-sslv3-urls-with-python-2-6-6-on-1-machine-but-not-wit
.. _#315: https://github.com/omab/django-social-auth/issues/315
