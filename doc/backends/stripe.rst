Stripe
======

Stripe uses OAuth2 for its authorization service. To setup Stripe backend:

- Register a new application at `Stripe App Creation`_, and

- Grab the ``client_id`` value in ``Applications`` tab and fill the ``App Id``
  setting::

    STRIPE_APP_ID = 'ca_...'

- Grab the ``Test Secret Key`` in the ``API Keys`` tab and fille the ``App
  Secret`` setting::

    STRIPE_APP_SECRET = '...'

- Define ``STRIPE_SCOPE`` with the desired scope (options are ``read_only`` and
  ``read_write``)::

    STRIPE_SCOPE = ['read_only']

- Add the needed backend to ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_auth.backends.stripe.StripeBackend',
        ...
    )

More info on Stripe OAuth2 at `Integrating OAuth`_.

.. _Stripe App Creation: https://manage.stripe.com/#account/applications/settings
.. _Integrating OAuth: https://stripe.com/docs/connect/oauth
