Vkontakte
=========
Vkontakte uses OAuth v2 for Authentication

- Register a new application at the `Vkontakte API`_, and

- fill ``App Id`` and ``Api Secret`` values in the settings::

      VK_APP_ID = ''
      VK_API_SECRET = ''

- Also it's possible to define extra permissions with::

     VK_EXTRA_SCOPE = [...]

  See the `names of the privileges VKontakte`_.

.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
.. _names of the privileges VKontakte: http://vk.com/developers.php?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
.. _Vkontakte API: http://vk.com/developers.php
