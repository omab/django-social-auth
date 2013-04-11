========
Facebook
========

Facebook works similar to Twitter but it's simpler to setup and redirect URL
is passed as a parameter when issuing an authorization. Further documentation
can be found at `Facebook development resources`_:

The steps below will get django-social-auth connected to your app running on *localhost*. 

#. Register a new application at `Facebook App Creation`_, follow along with the screenshots to setup your app:

#. .. image:: ../images/facebook_1.jpeg

#. .. image:: ../images/facebook_2.jpeg

#. Back to your django settings.py file, fill in the ``App ID`` and ``App Secret`` values from the blue box in step #3 ::

    FACEBOOK_APP_ID='App ID here'
    FACEBOOK_API_SECRET='App Secret here'

#. Make sure that you have the Facebook backend added to AUTHENTICATION_BACKENDS ::

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.facebook.FacebookBackend',
    )

#. You should now have Facebook enabled on localhost.


Facebook Extended Permissions
=============================

This is an optional step and only needed if you require extra information from Facebook such as email addresses, etc.  

- In django settings.py, define ``FACEBOOK_EXTENDED_PERMISSIONS`` to get extra permissions from facebook. For example, Facebook doesn't return user email by default, this setting is needed if email is required::

     FACEBOOK_EXTENDED_PERMISSIONS = ['email']

- Define ``FACEBOOK_PROFILE_EXTRA_PARAMS`` to pass extra parameters to
  https://graph.facebook.com/me when gathering the user profile data, like::

    FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

Facebook Canvas
===============

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
