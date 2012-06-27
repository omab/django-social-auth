GitHub
======
Github works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, set your site domain as
  the callback URL or it might cause some troubles when associating accounts,

- Fill ``App Id`` and ``App Secret`` values in the settings::

      GITHUB_APP_ID = ''
      GITHUB_API_SECRET = ''

- Also it's possible to define extra permissions with::

     GITHUB_EXTENDED_PERMISSIONS = [...]

.. _GitHub Developers: https://github.com/settings/applications/new
