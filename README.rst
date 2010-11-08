Django Social Auth
==================

1. Description
--------------
Basically this is a code merge between:
    * Django-Socialauth (https://github.com/uswaretech/Django-Socialauth)
    * django-twitter-oauth (https://github.com/henriklied/django-twitter-oauth)
the app supplies two views that controls OAuth and OpenID loggin/registration.

2. OAuth
-----------
Twitter and Facebook Oauth mechanims for authentication/registration,
corresponding apps and settings must be filled:

  - Twitter
    * Register a new app at http://twitter.com/apps/new
    * Be sure to mark the "Yes, use Twitter for login" checkbox
    * Fill "Cosumer Key" and "Consumer Secret" values in settings
        TWITTER_CONSUMER_KEY
        TWITTER_CONSUMER_SECRET
    Twitter demands a redirect url configuration and will force the user
    to that address when redirecting, I suggest to setup something like
    http://myvirtualapp.com and then configuring myvirtualapp.com in
    /etc/hosts file, the port will be missing but works well for testing.

  - Facebook
    * Register a new app at http://developers.facebook.com/setup/
    * Fill "App Id" and "App Secret" values in settings:
        FACEBOOK_APP_ID
        FACEBOOK_API_SECRET

3. OpenId
---------
Yahoo and Google OpenId providers are supported, also custom providers
like myopenid.com are supported if provider url is specified by a POST
parameter (openid_identifier).

4. Bugs
-------
Several, maybe, please report :-)

5. Copyrights
-------------
Base work is copyrighted by:

Oauth base code:
    Original Copyright goes to Henrik Lied (henriklied)
    Code borrowed from https://github.com/henriklied/django-twitter-oauth

OpenId base code:
    django-openid-auth -  OpenID integration for django.contrib.auth
    Copyright (C) 2007 Simon Willison
    Copyright (C) 2008-2010 Canonical Ltd.
