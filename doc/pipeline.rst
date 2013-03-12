Authentication Pipeline
=======================

The final process of the authentication workflow is handled by an operations
pipeline where custom functions can be added or default items can be removed to
provide a custom behavior.

The default pipeline mimics the user creation and basic data gathering from
previous django-social-auth_ versions and a big set of settings (listed below)
that were used to alter the default behavior are now deprecated in favor of
pipeline overrides.

The default pipeline is composed by::

    (
        'social_auth.backends.pipeline.social.social_auth_user',
        #'social_auth.backends.pipeline.associate.associate_by_email',
        'social_auth.backends.pipeline.user.get_username',
        'social_auth.backends.pipeline.user.create_user',
        'social_auth.backends.pipeline.social.associate_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

Email association (``associate_by_email`` pipeline entry) is disabled by
default for security reasons. Take for instance this scenario:

    1. User A registers using ``django-social-auth`` and we get email address
       ``foo@bar.com``.
    2. User B goes to provider XXX and registers using ``foo@bar.com``
       (provider XXX doesn't validate emails).
    3. User B goes to your site and logs in using its XXX account using
       ``django-social-auth``.
    4. User B gets access to User A account.

If this isn't a concern for your site, just define ``SOCIAL_AUTH_PIPELINE``
like the one shown above and uncomment the line for ``associate_by_email``.

But it's possible to override it by defining the setting
``SOCIAL_AUTH_PIPELINE``, for example a pipeline that won't create users, just
accept already registered ones would look like this::

    SOCIAL_AUTH_PIPELINE = (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.social.associate_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

Each pipeline function will receive the following parameters:
    * Current social authentication backend
    * User ID given by authentication provider
    * User details given by authentication provider
    * ``is_new`` flag (initialized in ``False``)
    * Any arguments passed to ``auth_complete`` backend method, default views
      pass this arguments:
        - current logged in user (if it's logged in, otherwise ``None``)
        - current request

Each pipeline entry can return a ``dict``, ``None`` or any form of
``HttpResponse`` (that includes ``HttpResponseRedirect`` too). If a ``dict`` was
returned, any value in the set will be merged into the ``kwargs`` argument for
the next pipeline entry, ``None`` is taken as if ``{}`` was returned, and if an
``HttpReponse`` instance was returned, it will halt the pipeline and the
response will be returned to the user (check **Partial Pipeline** section below).

The workflow will be cut if the exception ``social_auth.exceptions.StopPipeline``
is raised at any point.

If any function returns something else beside a ``dict`` or ``None``, the
workflow will be cut and the value returned immediately. This is useful to
return ``HttpReponse`` instances like ``HttpResponseRedirect``.


Partial Pipeline
----------------

It's possible to cut the pipeline process to return to the user asking for more
data and resume the process later. To accomplish this, add the entry
``social_auth.backends.pipeline.misc.save_status_to_session`` (or a similar
implementation) to the pipeline setting before any entry that returns an
``HttpResponse`` instance::

    SOCIAL_AUTH_PIPELINE = (
        ...
        social_auth.backends.pipeline.misc.save_status_to_session,
        app.pipeline.redirect_to_basic_user_data_form
        ...
    )

When it's time to resume the process just redirect the user to
``/complete/<backend>/`` view. By default the pipeline will be resumed in the
next entry after ``save_status_to_session``, but this can be modified by setting
the following setting to the import path of the pipeline entry to resume
processing::

    SOCIAL_AUTH_PIPELINE_RESUME_ENTRY = 'social_auth.backends.pipeline.misc.save_status_to_session'

``save_status_to_session`` saves needed data into user session. The key can be
defined by ``SOCIAL_AUTH_PARTIAL_PIPELINE_KEY``, which default value is
``partial_pipeline``::

    SOCIAL_AUTH_PARTIAL_PIPELINE_KEY = 'partial_pipeline'

Check the `example application`_ to check a basic usage.


.. _django-social-auth: https://github.com/omab/django-social-auth
.. _example application: https://github.com/omab/django-social-auth/blob/master/example/example/local_settings.py.template#L23
