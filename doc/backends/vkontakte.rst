VKontakte
=========
VKontakte uses OAuth v2 for Authentication

- Register a new application at the `Vkontakte API`_, and

- fill ``App Id`` and ``Api Secret`` values in the settings::

      VK_APP_ID = ''
      VK_API_SECRET = ''

- Also it's possible to define extra permissions with::

     VK_EXTRA_SCOPE = [...]

  See the `names of the privileges VKontakte`_.

You can also use VKontakte's own OpenAPI to log in, but you need to provide HTML template
with JavaScript code to authenticate. See vkontakte.html in templates folder for details.

To support authentication for VKontakte applications:

    * Create your IFrame application at VKontakte.
    * In application settings specify your IFrame URL mysite.com/vk (current default).
    * Because VKontakte IFrame uses different app ID, you have to specify it and secret key in VKONTAKTE_APP_AUTH setting
    * VKONTAKTE_APP_AUTH={'key':'iframe_app_secret_key', 'user_mode': 2, 'id':'iframe_app_id'}
    * user_mode values:
        - 0: there will be no check whether a user connected to your application or not
        - 1: DSA will check is_app_user parameter VKontakte sends when user opens app page one time
        - 2 (safest) DSA will check status of user interactively (useful when you have interactive authentication via AJAX)
    * Launch manage.py via sudo ./manage.py mysite.com:80 for browser to be able to load it when VKontakte calls IFrame URL.
    * Open your VKontakte app page via http://vk.com/app"app_id"
    * Now you are able to connect to application and login automatically after connection when visiting application page.

For more details see `authentication for VKontakte applications`_

.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
.. _names of the privileges VKontakte: http://vk.com/developers.php?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
.. _Vkontakte API: http://vk.com/developers.php
.. _authentication for VKontakte applications: http://www.ikrvss.ru/2011/11/08/django-social-auh-and-vkontakte-application/