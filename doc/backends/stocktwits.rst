StockTwits
^^^^^^^^^^

StockTwits uses OAuth 2 for authentication.

- Register a new application at https://stocktwits.com/developers/apps

- Set the Website URL to http://[your domain]/

- fill ``Consumer Key`` and ``Consumer Secret`` values in your django settings::

      STOCKTWITS_CONSUMER_KEY    = ''
      STOCKTWITS_CONSUMER_SECRET = ''

.. _StockTwits authentication docs: http://stocktwits.com/developers/docs/authentication
.. _StockTwits API: http://stocktwits.com/developers/docs/api
