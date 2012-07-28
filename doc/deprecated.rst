Deprecated bits
===============

The following settings are deprecated in favor of pipeline functions.

- These old settings aren't supported anymore, override ``get_username``
  pipeline entry with the desired behavior::

    SOCIAL_AUTH_FORCE_RANDOM_USERNAME
    SOCIAL_AUTH_DEFAULT_USERNAME
    SOCIAL_AUTH_UUID_LENGTH
    SOCIAL_AUTH_USERNAME_FIXER
    SOCIAL_AUTH_ASSOCIATE_URL_NAME

- User creation setting was removed, remove the entry ``create_user``
  from pipeline instead::

    SOCIAL_AUTH_CREATE_USERS

  Also the signal ``socialauth_not_registered`` was removed.

- Automatic data update is the default behavior, this old setting was removed::

    SOCIAL_AUTH_CHANGE_SIGNAL_ONLY

  Override ``update_user_details`` if needed.

- Extra data retrieval is default behavior, this setting is not supported any
  more::

    SOCIAL_AUTH_EXTRA_DATA

  Remove ``load_extra_data`` from pipeline if needed.

- Automatic email association is disabled by default since it could be
  a security risk and allow users to take-over others accounts by spoofing
  email address in providers. Also this setting is not supported any more::

    SOCIAL_AUTH_ASSOCIATE_BY_MAIL

- Associate URLs are deprecated since the login ones can handle the case, this
  avoids issues where providers check the redirect URI and redirects to the
  configured value in the application. So, from now on a single entry point is
  recommended being::

        /<social auth path>/login/<backend>/

  And to complete the process::

        /<social auth path>/complete/<backend>/
