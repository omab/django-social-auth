VK.com
=========

VK.com auth service supported.

OAuth2
------

VKontakte uses OAuth2 for Authentication.

- Register a new application at the `Vkontakte API`_,

- fill ``Application Id`` and ``Application Secret`` values in the settings::

      VK_APP_ID = ''
      VK_API_SECRET = ''

- Add ``'social_auth.backends.contrib.vk.VKOAuth2Backend'`` into your ``AUTHENTICATION_BACKENDS``.

- Then you can start using ``{% url 'socialauth_begin' 'vk-oauth' %}`` in your templates

- Also it's possible to define extra permissions with::

     VK_EXTRA_SCOPE = [...]

  See the `VK.com list of permissions`_.


OpenAPI
-------

You can also use VK.com's own OpenAPI to log in, but you need to provide
HTML template with JavaScript code to authenticate. See ``vkontakte.html`` in
templates folder for details.

IFrame Applications
-------------------

To support authentication for VKontakte applications:

- Fill ``Application ID`` and ``Application Secret`` settings::

    VKAPP_APP_ID = <APP ID>
    VKAPP_API_SECRET = <APP SECRET>

- Create your IFrame application at vk.com.

- In application settings specify your IFrame URL ``mysite.com/vk`` (current
  default).

- You may need to also provide VKAPP_USER_MODE setting (0 by default)

  * ``VKAPP_USER_MODE`` values:

    - ``0``: there will be no check whether a user connected to your
      application or not
    - ``1``: ``Django-social-auth`` will check ``is_app_user`` parameter
      VKontakte sends when user opens application page one time
    - ``2``: (safest) ``Django-social-auth`` will check status of user
      interactively (useful when you have interactive authentication via AJAX)

- To test, launch the server using ``sudo ./manage.py mysite.com:80`` for
  browser to be able to load it when VKontakte calls IFrame URL.

- Open your VK.com application page via http://vk.com/app<app_id>

- Now you are able to connect to application and login automatically after
  connection when visiting application page.

For more details see `authentication for VKontakte applications`_

.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
.. _VK.com list of permissions: http://vk.com/developers.php?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
.. _Vkontakte API: http://vk.com/developers.php
.. _authentication for VKontakte applications: http://www.ikrvss.ru/2011/11/08/django-social-auh-and-vkontakte-application/
