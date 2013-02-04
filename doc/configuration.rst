Configuration
=============

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
        'social_auth.backends.contrib.vkontakte.VKontakteBackend',
        'social_auth.backends.contrib.live.LiveBackend',
        'social_auth.backends.contrib.skyrock.SkyrockBackend',
        'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
        'social_auth.backends.OpenIDBackend',
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
    VK_APP_ID                    = ''
    VK_API_SECRET                = ''
    LIVE_CLIENT_ID = ''
    LIVE_CLIENT_SECRET = ''
    SKYROCK_CONSUMER_KEY      = ''
    SKYROCK_CONSUMER_SECRET   = ''
    YAHOO_CONSUMER_KEY        = ''
    YAHOO_CONSUMER_SECRET     = ''


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
        'social_auth.context_processors.social_auth_login_redirect',
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

  * ``social_auth_login_redirect``:
    For man in the middle redirects (ie authenticating via a login
    required decorator), a convenince query string can be added to your context
    for templates. On your login options page::

        <a href={% url socialauth_begin 'twitter' %}?{{ redirect_querystring }}">...</a>

    allows for a continuous login. Useful if multiple login options are
    presented.

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

- The update_user_details pipeline processor will set certain fields on user
  objects, such as ``email``. Set this to a list of fields you only want to
  set for newly created users:

    SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]

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

- You can send extra parameters on auth process by defining settings per
  provider, example to request Facebook to show Mobile authorization page,
  define::

      FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'touch'}

  For other providers, just define settings in the form::

      <uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}

  You can override the arguments defined in the settings with GET parameters.

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

    SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.log_exceptions_to_messages'

  The function parameters are ``request`` holding the current request object,
  ``backend`` with the current backend and ``err`` which is the exception
  instance. If the function returns a URL, the user will be redirected to it.
  Otherwise, they will be redirected to the backend's error URL, or
  ``LOGIN_ERROR_URL``.

  Recently this set of exceptions was introduced to describe the situations
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
    AuthAlreadyAssociated   - A different user has already associated
                              the social account that the current user
                              is trying to associate. 

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

- The name of the last backend used to login is stored as a string in the
  session under the key ``social_auth_last_login_backend``, the key can be
  customized by defining this setting::

    SOCIAL_AUTH_LAST_LOGIN = 'social_auth_last_login_backend'

- Any ``urllib2.urlopen`` call will be performed with the default timeout
  value, to change it without affecting the global socket timeout define this
  setting (the value specifies timeout seconds)::

    SOCIAL_AUTH_URLOPEN_TIMEOUT = 30

  ``urllib2.urlopen`` uses ``socket.getdefaulttimeout()`` value by default, so
  setting ``socket.setdefaulttimeout(...)`` will affect ``urlopen`` when this
  setting is not defined, otherwise this setting takes precedence. Also this
  might affect other places in Django.

  ``timeout`` argument was introduced in python 2.6 according to `urllib2
  documentation`_


- `OpenID PAPE`_ extension support by defining::

    SOCIAL_AUTH_OPENID_PAPE_MAX_AUTH_AGE = <int value>

  Otherwise the extension is not used.

Some settings can be tweak by backend by adding the backend name prefix (all
uppercase and replace ``-`` with ``_``), here's the supported settings so far::

        LOGIN_ERROR_URL
        SOCIAL_AUTH_BACKEND_ERROR_URL
        SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL
        SOCIAL_AUTH_DISCONNECT_REDIRECT_URL
        SOCIAL_AUTH_NEW_USER_REDIRECT_URL
        SOCIAL_AUTH_LOGIN_REDIRECT_URL
        SOCIAL_AUTH_INACTIVE_USER_URL

- The ORM models can be replaced by providing the name of an alternate module
  for the ``SOCIAL_AUTH_MODELS`` setting. The default is
  ``'social_auth.db.django_models'``, which defines the Django ORM models that
  were originally defined to implement Social Auth's storage. The app provides
  an example alternate based on `MongoEngine`_. You can use it by setting::

    SOCIAL_AUTH_MODELS = 'social_auth.db.mongoengine_models'

  Make sure you've followed the instructions for `MongoEngine Django
  integration`_, as you're now utilizing that user model.

  The `MongoEngine_` backend was developed and tested with version 0.6.10 of
  `MongoEngine_`.

  Alternate storage models implementations currently follow a tight pattern of
  models that behave near or identical to Django ORM models. It is currently
  not decoupled from this pattern by any abstraction layer. If you would like
  to implement your own alternate, please see the
  ``social_auth.db.django_models`` and ``social_auth.db.mongoengine_models``
  modules for guidance.

- A base middleware is provided that handles social ``AuthExceptions`` by
  providing a message to the user via the Django messages framework, and then
  responding with a redirect to a URL defined by one of the middleware methods.
  The base middleware is
  ``social_auth.middleware.SocialAuthExceptionMiddleware``. The two methods to
  override when subclassing are ``get_message(request, exception)`` and
  ``get_redirect_uri(request, exception)``. By default, the message is the
  exception message and the URL for the redirect is the location specified by
  the ``LOGIN_ERROR_URL`` configuration setting.


Notes
-----

Since Django 1.3 the URL templatetag ``{% url socialauth_begin ... %}`` syntax
is deprecated in favor the new format where the URL name is quoted (using
single quotes). See the `release notes`_ for details.

The new syntax is not enforced yet but will be on Django 1.5 (current trunk),
and it's also available by importing ``url`` tag from ``future`` module doing::

    {% load url from future %}

In case of experiencing issues similar to `#303`_, check the tag being used and
its syntax.


.. _Model Manager: http://docs.djangoproject.com/en/dev/topics/db/managers/#managers
.. _Login URL: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-url
.. _Login redirect URL: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#login-redirect-url
.. _AUTHENTICATION_BACKENDS: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#authentication-backends
.. _auth.User: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py#L186
.. _auth.UserManager: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py#L114
.. _login_required: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/decorators.py#L39
.. _User Profiles: http://www.djangobook.com/en/1.0/chapter12/#cn222
.. _OAuth: http://oauth.net/
.. _MongoEngine: http://mongoengine.org
.. _MongoEngine Django integration: http://mongoengine-odm.readthedocs.org/en/latest/django.html
.. _urllib2 documentation: http://docs.python.org/library/urllib2.html#urllib2.urlopen
.. _release notes: https://docs.djangoproject.com/en/1.3/releases/1.3/#changes-to-url-and-ssi
.. _#303: https://github.com/omab/django-social-auth/issues/303
.. _OpenID PAPE: http://openid.net/specs/openid-provider-authentication-policy-extension-1_0.html
