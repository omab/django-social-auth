Douban
======

Douban OAuth
------------
Douban OAuth works similar to Twitter.

Douban offers per application keys named ``Consumer Key`` and ``Consumer
Secret``. To enable Douban OAuth these two keys are needed. Further
documentation at `Douban Services & API`_:

- Register a new application at `DOUBAN API KEY`_,

- Mark the **web application** checkbox.

- Fill **Consumer Key** and **Consumer Secret** values in settings::

      DOUBAN_CONSUMER_KEY
      DOUBAN_CONSUMER_SECRET

- Add ``'social_auth.backends.contrib.douban.DoubanBackend'``
  into your ``AUTHENTICATION_BACKENDS``.

- Then you can start using ``{% url socialauth_begin 'douban' %}`` in your
  templates


Douban OAuth2
-------------
Recently Douban launched their OAuth2 support and the new developer site, you
can find documentation at `Douban Developers`_:

- Register a new application at `Create A Douban App`_,

- Mark the **web application** checkbox.

- Fill **Consumer Key** and **Consumer Secret** values in settings::

      DOUBAN2_CONSUMER_KEY
      DOUBAN2_CONSUMER_SECRET

- Add ``'social_auth.backends.contrib.douban.DoubanBackend2'``
  into your ``AUTHENTICATION_BACKENDS``.

- Then you can start using ``{% url socialauth_begin 'douban2' %}`` in your
  templates.

.. _Douban Services & API: http://www.douban.com/service/
.. _Douban API KEY: http://www.douban.com/service/apikey/apply
.. _Douban Developers : http://developers.douban.com/
.. _Create A Douban App : http://developers.douban.com/apikey/apply
