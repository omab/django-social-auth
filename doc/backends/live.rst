MSN Live Connect
================
OAuth2 based Live Connect workflow, notice that it isn't OAuth WRAP.

- Register a new application at `Live Connect Developer Center`_, set your site domain as
  redirect domain,

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      LIVE_CLIENT_ID = ''
      LIVE_CLIENT_SECRET = ''

- Also it's possible to define extra permissions with::

     LIVE_EXTENDED_PERMISSIONS = [...]

  Defaults are "wl.basic" and "wl.emails". Latter one is necessary to retrieve user email.

.. _Live Connect Developer Center: https://manage.dev.live.com/Applications/Index
