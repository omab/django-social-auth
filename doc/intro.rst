Introduction
============

Django Social Auth is an easy to setup social authentication/authorization
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
    * `Vkontakte OAuth`_

- Basic user data population and signaling, to allows custom fields values
  from providers response

- Multiple social accounts association to single users

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
.. _Twitter OAuth: http://dev.twitter.com/pages/oauth_faq
.. _Facebook OAuth: http://developers.facebook.com/docs/authentication/
.. _Linkedin OAuth: https://www.linkedin.com/secure/developer
.. _Orkut OAuth:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _myOpenID: https://www.myopenid.com/
.. _LiveJournal OpenID: http://www.livejournal.com/support/faqbrowse.bml?faqid=283
.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
