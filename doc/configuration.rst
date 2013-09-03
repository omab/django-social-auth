Configuration
=============

Application Setup
-----------------

- Add social_auth to ``PYTHONPATH`` and installed applications::

    INSTALLED_APPS = (
        ...
        'social_auth'
    )

- Sync database to create needed models::

    ./manage.py syncdb

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
        'social_auth.backends.contrib.disqus.DisqusBackend',
        'social_auth.backends.contrib.livejournal.LiveJournalBackend',
        'social_auth.backends.contrib.orkut.OrkutBackend',
        'social_auth.backends.contrib.foursquare.FoursquareBackend',
        'social_auth.backends.contrib.github.GithubBackend',
        'social_auth.backends.contrib.vk.VKOAuth2Backend',
        'social_auth.backends.contrib.live.LiveBackend',
        'social_auth.backends.contrib.skyrock.SkyrockBackend',
        'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
        'social_auth.backends.contrib.readability.ReadabilityBackend',
        'social_auth.backends.contrib.fedora.FedoraBackend',
        'social_auth.backends.OpenIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

  Take into account that backends **must** be defined in AUTHENTICATION_BACKENDS_
  or Django won't pick them up when trying to authenticate the user.

  Don't miss ``django.contrib.auth.backends.ModelBackend`` if using ``django.contrib.auth``
  User model or users won't be able to login.

- Add URLs entries::

    urlpatterns = patterns('',
        ...
        url(r'', include('social_auth.urls')),
        ...
    )

  All ``django-social-auth`` URLs names have ``socialauth_`` prefix.


Keys and Secrets
----------------

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
    LIVE_CLIENT_ID               = ''
    LIVE_CLIENT_SECRET           = ''
    SKYROCK_CONSUMER_KEY         = ''
    SKYROCK_CONSUMER_SECRET      = ''
    YAHOO_CONSUMER_KEY           = ''
    YAHOO_CONSUMER_SECRET        = ''
    READABILITY_CONSUMER_SECRET  = ''
    READABILITY_CONSUMER_SECRET  = ''


URLs Options
------------

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

- Inactive users can be redirected to a different page if this setting is
  defined::

      SOCIAL_AUTH_INACTIVE_USER_URL = '...'

  Defaults to ``LOGIN_ERROR_URL``.


Custom User Model
-----------------

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

  These are needed to ensure a better ``django-auth`` integration, otherwise
  `login_required`_ won't be usable. A warning is displayed if any of these are
  missing. By default `auth.User`_ is used.

  Check the example application for implementation details, but first, please take
  a look at `User Profiles`_. It might be what you are looking for.


ORMs
----

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


Tweaking Some Fields Length
---------------------------

Some databases impose limitations to indexes columns (like MySQL InnoDB),
these limitations won't play nice on some `UserSocialAuth` fields. To avoid
such errors, define some of the following settings.

- Provider UID::

    SOCIAL_AUTH_UID_LENGTH = <int>

  Which will be used to define the field `uid` `max_length`. A value of 223
  should work when using MySQL InnoDB which imposes a 767 byte limit (assuming
  UTF-8 encoding).

- Association and Nonce keys:

  ``Association`` and ``Nonce`` models have composed keys by a unique
  constraint.

  ``Nonce`` models has a ``unique_together`` constraint over
  ``('server_url', 'timestamp', 'salt')``, salt has a max length of 40, so
  ``server_url`` length must be tweaked using::

    SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = <int>

  ``Association`` models has a ``unique_together`` constraint over
  ``('server_url', 'handle')``, and both fields lengths can be tweaked by these
  settings::

    SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = <int>
    SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = <int>


Username Generation
-------------------

- Used to build a default username if provider didn't returned any useful
  value::

    SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

  or::

    import random
    SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])

  in case your user layout needs to purify username on some way.

  Final user name will have a random UUID-generated suffix in case it's already
  taken. The UUID token max length can be changed with the setting::

    SOCIAL_AUTH_UUID_LENGTH = 16

- For those that prefer slugged usernames, the `get_username` pipeline can
  apply slugify from django tools by defining this setting::

    SOCIAL_AUTH_SLUGIFY_USERNAMES = True

  The feature is disabled by default to keep backward compatibility and to not
  force this option on projects where Unicode usernames are a valid choice.

  If Django ``slugify`` function doesn't fit your project, it always possible
  to override it by defining this setting::

    SOCIAL_AUTH_SLUGIFY_FUNCTION = 'import.path.to.your.slugify'

- If you want to use the full email address as the ``username``, define this setting::

    SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

  Make sure you don't use the ``SOCIAL_AUTH_SLUGIFY_USERNAMES = True`` option
  described above, as the ``@`` sign will be removed.


Extra Arguments on Auth Processes
---------------------------------

- You can send extra parameters on auth process by defining settings per
  backend, example to request Facebook to show Mobile authorization page,
  define::

      FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'touch'}

  For other providers, just define settings in the form::

      <uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}

  You can override the arguments defined in the settings with GET parameters.

- Also, you can send extra parameters on request token process by defining
  settings per provider in the same way explained above but with this other
  suffix::

      <uppercase backend name>_REQUEST_TOKEN_EXTRA_ARGUMENTS = {...}


Processing Redirects and urlopen
--------------------------------

- By default the application doesn't make redirects to different domains, to
  disable this behavior::

      SOCIAL_AUTH_SANITIZE_REDIRECTS = False

- When your project is behind a reverse proxy that uses HTTPS the redirect URIs
  can became with the wrong schema (``http://`` instead of ``https://``), and
  might cause errors with the auth process, to force HTTPS in the final URIs
  define this setting::

    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

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


Per-backend Settings
--------------------

Some settings can be tweak by backend by adding the name as a prefix (all
uppercase and replace ``-`` with ``_``), here's the supported settings so far::

        LOGIN_ERROR_URL
        SOCIAL_AUTH_BACKEND_ERROR_URL
        SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL
        SOCIAL_AUTH_DISCONNECT_REDIRECT_URL
        SOCIAL_AUTH_NEW_USER_REDIRECT_URL
        SOCIAL_AUTH_LOGIN_REDIRECT_URL
        SOCIAL_AUTH_INACTIVE_USER_URL


Exceptions
----------

- This set of exceptions was introduced to describe the situations a bit more
  than the old ``ValueError`` usually raised::

    SocialAuthBaseException - Base class for all social auth exceptions
    AuthException           - Base exception class for authentication process
                              errors
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
    WrongBackend            - Raised when the backend given in the URLs is
                              invalid (not enabled or registered)
    NotAllowedToDisconnect  - Raised on disconnect action when it's not safe
                              for the user to disconnect the social account,
                              probably because the user lacks a password or
                              another social account
    StopPipeline            - Used internally by pipelines to stop the halt the
                              process
    AuthStateMissing        - The state parameter is missing from the server
                              response
    AuthStateForbidden      - The state parameter returned by the server is not
                              the one sent
    AuthTokenRevoked        - Raised when the user revoked the access_token in
                              the provider

  These are subclasses of ``ValueError`` to keep backward compatibility.


Exceptions Middleware
---------------------

- A base middleware is provided that handles ``SocialAuthBaseException`` by
  providing a message to the user via the Django messages framework, and then
  responding with a redirect to a URL defined by one of the middleware methods.
  The base middleware is ``social_auth.middleware.SocialAuthExceptionMiddleware``.
  The two methods to override when subclassing are::

    get_message(request, exception)
    get_redirect_uri(request, exception)

  By default, the message is the exception message and the URL for the redirect
  is the location specified by the ``LOGIN_ERROR_URL`` configuration setting.

  If a valid backend was detected by ``dsa_view()`` decorator, it will be
  available at ``request.social_auth_backend`` and ``process_exception()`` will
  use it to build a backend-dependent redirect URL.

  Exception processing is disabled if any of this settings is defined with
  a ``True`` value::

    <backend name>_SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    SOCIAL_AUTH_RAISE_EXCEPTIONS = True


Template Context Processors
---------------------------

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
    For man-in-the-middle redirects (ie authenticating via a login
    required decorator), a convenince query string can be added to your context
    for templates. On your login options page::

        <a href="{% url 'socialauth_begin' 'twitter' %}?{{ redirect_querystring }}">...</a>

    allows for a continuous login. Useful if multiple login options are
    presented.

  Check ``social_auth.context_processors`` for details.

  **Note**:
  ``social_auth_backends`` and ``social_auth_by_type_backends`` don't play nice
  together.


Miscellaneous Settings
----------------------

- Disconnect is an side-effect operation and should be protected against CSRF
  attacks, but for historical reasons it wasn't and by default it's kept that
  way. To force CSRF protection define::

    SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

  And ensure that any call to `/disconnect/foobar/` or `/disconnect/foobar/<id>/`
  is done using POST. A 405 status code will be returned if the URL is not loaded
  with a POST method. Also ensure that a CSRF token is sent in the request.

- The update_user_details pipeline processor will set certain fields on user
  objects, such as ``email``. Set this to a list of fields you only want to
  set for newly created users::

    SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]

  Also more extra values will be stored if defined. Details about this setting
  are listed below in the OpenId and OAuth sections.

- Some providers return the time that the access token will live, and the value is
  stored in ``UserSocialAuth.extra_data`` under the key ``expires``. By default
  the current user session is set to expire if this value is present. This
  behavior can be disabled by setting::

    SOCIAL_AUTH_SESSION_EXPIRATION = False

- If you want to store extra parameters from POST or GET in session, like it
  was made for ``next`` parameter, define this setting::

      SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['foo',]

  In this case the ``foo`` field's value will be stored when user follows this link
  ``<a href="{% url 'socialauth_begin' 'github' %}?foo=bar">...</a>``.

- `OpenID PAPE`_ extension support by defining::

    SOCIAL_AUTH_OPENID_PAPE_MAX_AUTH_AGE = <int value>

  Otherwise the extension is not used.

- If you want to revoke a provider's tokens on disconnect, define this setting::

    SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True

  Currently only handled for Facebook and Google-OAuth2. Some providers (e.g. Twitter)
  do not support revoking tokens from your app at all.


Linking in your templates
-------------------------

Not at configuration actually. To link your clients to start the process, just
add this to your template::

    {% url "socialauth_begin" "backend-name" %}

Backend name can be found on ``BACKENDS`` attribute in the backend module. The
same URL works for association accounts for logged in users.

For social account disconnection, there are two URLs, one to disconnect all
social accounts for a given backend (not really useful IMO)::

    {% url "socialauth_disconnect" "backend-name" %}

Or to disconnect individual accounts::

    {% url "socialauth_disconnect_individual" "backend-name" association_id %}

For example, given a ``UserSocialAuth`` instance under the name ``social`` in
templates context, you can create a link to disconnect that association with::

    <a href="{% url "socialauth_disconnect_individual" social.provider social.id %}">Disconnect {{ social.provider }}</a>

or disconnect all association for given provider with::

    <a href="{% url "socialauth_disconnect" social.provider %}">Disconnect {{ social.provider }}</a>

You can set SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT to True if you wish to revoke
tokens on disconnect (only some backends support this).

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
.. _OpenID PAPE: http://openid.net/specs/openid-provider-authentication-policy-extension-1_0.html
