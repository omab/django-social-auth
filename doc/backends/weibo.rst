Weibo OAuth
===========

Weibo OAuth 2.0 workflow.

- Register a new application at Weibo_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      WEIBO_CLIENT_KEY = ''
      WEIBO_CLIENT_SECRET = ''

By default account id, profile_image_url, gender are stored in extra_data
field, check OAuthBackend class for details on how to extend it.

.. _Weibo: http://open.weibo.com
