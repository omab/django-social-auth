Shopify
^^^^^^^

Shopify uses OAuth 2 for authentication.

To use this backend, you must install the package ``shopify`` (`Github`_)

- Register a new application at `Shopify Partners`_, and

- Set the Auth Type to OAuth2 in the application settings

- Set the Application URL to http://[your domain]/social/login/shopify/

- fill ``API Key`` and ``Shared Secret`` values in your django settings::

      SHOPIFY_APP_API_KEY   = ''
      SHOPIFY_SHARED_SECRET = ''

- fill the scope permissions that you require into the settings `Shopify API`_::

      SHOPIFY_SCOPE = ["write_script_tags","read_orders","write_customers","read_products"]

.. _Shopify Partners: http://www.shopify.com/partners
.. _Shopify API: http://api.shopify.com/authentication.html#scopes
.. _Github: https://github.com/Shopify/shopify_python_api
