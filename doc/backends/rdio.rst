Rdio
====

OAuth 1.0a
----------

To setup Rdio OAuth 1.0a, add the following to your settings page::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_auth.backends.contrib.rdio.RdioOAuth1Backend',
        ...
    )

    RDIO_OAUTH1_KEY = os.environ['RDIO_OAUTH1_KEY']
    RDIO_OAUTH1_SECRET = os.environ['RDIO_OAUTH1_SECRET']


OAuth 2.0
---------

To setup Rdio OAuth 2.0, add the following to your settings page::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_auth.backends.contrib.rdio.RdioOAuth2Backend',
        ...
    )

    RDIO_OAUTH2_KEY = os.environ['RDIO_OAUTH2_KEY']
    RDIO_OAUTH2_SECRET = os.environ['RDIO_OAUTH2_SECRET']
    RDIO2_PERMISSIONS = []


Extra Fields
------------

The following extra fields are automatically requested:

- rdio_id
- rdio_icon_url
- rdio_profile_url
- rdio_username
- rdio_stream_region
