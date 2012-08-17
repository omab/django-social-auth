Introduction
============

Django Social Auth is an easy way to setup social authentication/authorization
mechanism for Django projects.

Crafted using base code from django-twitter-oauth_ and django-openid-auth_,
implements a common interface to define new authentication providers from
third parties.


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
    * `Flickr OAuth`_
    * `Vkontakte OAuth`_
    * `MSN Live Connect OAuth2`_
    * `Skyrock OAuth`_
    * `Yahoo OAuth`_
    * `Evernote OAuth`_
    * `Mail.ru OAuth`_
    * `Odnoklassniki OAuth`_ and `Odnoklassniki IFrame applications`_
    * `Mixcloud OAuth2`_
    * `BitBucket OAuth`_
    * `Douban OAuth`_
    * `Fitbit OAuth`_
    * `Instagram OAuth2`_
    * `Twilio`_
    * `Weibo OAuth2`_
    * `Yandex OpenId`_

- Basic user data population and signaling, to allows custom fields values
  from providers response

- Multiple social account associations to a single user

- Custom User model override if needed (`auth.User`_ by default)

- Extensible pipeline to handle authentication/association mechanism

.. _auth.User: http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py#L186
.. _OpenId: http://openid.net/
.. _OAuth: http://oauth.net/
.. _django-twitter-oauth: https://github.com/henriklied/django-twitter-oauth
.. _django-openid-auth: https://launchpad.net/django-openid-auth
.. _Google OpenID: http://code.google.com/apis/accounts/docs/OpenID.html
.. _Google OAuth: http://code.google.com/apis/accounts/docs/OAuth.html
.. _Google OAuth2: http://code.google.com/apis/accounts/docs/OAuth2.html
.. _Yahoo OpenID: http://openid.yahoo.com/
.. _myOpenID: https://www.myopenid.com/
.. _Twitter OAuth: http://dev.twitter.com/pages/oauth_faq
.. _Facebook OAuth: http://developers.facebook.com/docs/authentication/
.. _LiveJournal OpenID: http://www.livejournal.com/support/faqbrowse.bml?faqid=283
.. _Orkut OAuth:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _Linkedin OAuth: https://www.linkedin.com/secure/developer
.. _Foursquare OAuth2: https://developer.foursquare.com/docs/oauth.html
.. _GitHub OAuth: http://developer.github.com/v3/oauth/
.. _Dropbox OAuth: https://www.dropbox.com/developers_beta/reference/api
.. _Flickr OAuth: http://www.flickr.com/services/api/
.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
.. _MSN Live Connect OAuth2: http://msdn.microsoft.com/en-us/library/live/hh243647.aspx
.. _Skyrock OAuth: http://www.skyrock.com/developer/
.. _Yahoo OAuth: http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html
.. _Evernote OAuth: http://dev.evernote.com/documentation/cloud/chapters/Authentication.php
.. _Mail.ru OAuth: http://api.mail.ru/docs/guides/oauth/
.. _Odnoklassniki OAuth: http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=12878032
.. _Odnoklassniki IFrame applications: http://dev.odnoklassniki.ru/wiki/display/ok/Odnoklassniki.ru+Third+Party+Platform
.. _Mixcloud OAuth2: http://www.mixcloud.com/developers/documentation/#authorization
.. _BitBucket OAuth: https://confluence.atlassian.com/display/BITBUCKET/OAuth+Consumers
.. _Douban OAuth: http://www.douban.com/service/apidoc/auth
.. _Fitbit OAuth: https://wiki.fitbit.com/display/API/OAuth+Authentication+in+the+Fitbit+API
.. _Instagram OAuth2: http://instagram.com/developer/authentication/
.. _Twilio: https://www.twilio.com/user/account/connect/apps
.. _Weibo OAuth2: http://open.weibo.com/wiki/Oauth2
.. _Yandex OpenId: http://openid.yandex.ru/
