Authentication Pipeline
=======================

The final process of the authentication workflow is handled by a operations
pipeline where custom functions can be added or default items can be removed to
provide a custom behavior.

The default pipeline mimics the user creation and basic data gathering from
previous django-social-auth_ versions and a big set of settings (listed below)
that were used to alter the default behavior are now deprecated in favor of
pipeline overrides.

The default pipeline is composed by::

    (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.associate.associate_by_email',
        'social_auth.backends.pipeline.user.get_username',
        'social_auth.backends.pipeline.user.create_user',
        'social_auth.backends.pipeline.social.associate_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

But it's possible to override it by defining the setting
``SOCIAL_AUTH_PIPELINE``, for example a pipeline that won't create users, just
accept already registered ones would look like this::

    SOCIAL_AUTH_PIPELINE = (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

Each pipeline function will receive the following parameters:
    * Current social authentication backend
    * User ID given by authentication provider
    * User details given by authentication provider
    * ``is_new`` flag (initialized in False)
    * Any arguments passed to ``auth_complete`` backend method, default views
      pass this arguments:
        - current logged in user (if it's logged in, otherwise ``None``)
        - current request

Each pipeline entry must return a ``dict`` or ``None``, any value in the
``dict`` will be used in the ``kwargs`` argument for the next pipeline entry.

The workflow will be cut if the exception ``social_auth.backends.exceptions.StopPipeline``
is raised at any point.

If any function returns something else beside a ``dict`` or ``None``, the
workflow will be cut and the value returned immediately, this is useful to
return ``HttpReponse`` instances like ``HttpResponseRedirect``.


.. _django-social-auth: https://github.com/omab/django-social-auth
