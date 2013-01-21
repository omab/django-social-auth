Facebook
========

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

If you need to perform authentication from Facebook Canvas application:
    - Create your canvas application at http://developers.facebook.com/apps
    - In Facebook application settings specify your canvas URL
      ``mysite.com/fb`` (current default)
    - Setup your Django Social Auth settings like you usually do for Facebook
      authentication (FACEBOOK_APP_ID etc)
    - Launch manage.py via sudo ``./manage.py runserver mysite.com:80`` for
      browser to be able to load it when Facebook calls canvas URL
    - Open your Facebook page via http://apps.facebook.com/app_namespace or
      better via http://www.facebook.com/pages/user-name/user-id?sk=app_app-id
    - After that you will see this page in a right way and will able to connect
      to application and login automatically after connection

More info on the topic at `Facebook Canvas Application Authentication`_.

.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/
.. _Facebook Canvas Application Authentication: http://www.ikrvss.ru/2011/09/22/django-social-auth-and-facebook-canvas-applications/
