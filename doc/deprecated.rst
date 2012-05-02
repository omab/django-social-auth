Deprecated bits
===============

The following settings are deprecated in favor of pipeline functions.

- These settings should be avoided and override ``get_username`` pipeline entry
  with the desired behavior::

    SOCIAL_AUTH_FORCE_RANDOM_USERNAME
    SOCIAL_AUTH_DEFAULT_USERNAME
    SOCIAL_AUTH_UUID_LENGTH
    SOCIAL_AUTH_USERNAME_FIXER
    SOCIAL_AUTH_ASSOCIATE_URL_NAME

- User creation setting should be avoided and remove the entry ``create_user``
  from pipeline instead::

    SOCIAL_AUTH_CREATE_USERS

- Automatic data update should be stopped by overriding ``update_user_details``
  pipeline entry instead of using this setting::

    SOCIAL_AUTH_CHANGE_SIGNAL_ONLY

- Extra data retrieval from providers should be stopped by removing
  ``load_extra_data`` from pipeline instead of using this setting::

    SOCIAL_AUTH_EXTRA_DATA

- Automatic email association should be avoided by removing
  ``associate_by_email`` pipeline entry instead of using this setting::

    SOCIAL_AUTH_ASSOCIATE_BY_MAIL

- Associate URLs are deprecated since the login ones can handle the case, this
  avoids issues where providers check the redirect URI and redirects to the
  configured value in the application. So, from now on a single entry point is
  recommended being::

        /<social auth path>/login/<backend>/

  And to complete the process::

        /<social auth path>/complete/<backend>/
