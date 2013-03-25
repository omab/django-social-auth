Reddit
======

Reddit implements `OAuth2 authentication workflow`_. To enable it, just follow:

- Register an application at `Reddit Preferences Apps`_

- Fill the **Consumer Key** and **Consumer Secret** values in your settings::

    REDDIT_APP_ID = ''
    REDDIT_API_SECRET = ''

- By default the token is not permanent, it will last an hour. To get
  a refresh token just define::

    REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

  This will store the ``refresh_token`` in ``UserSocialAuth.extra_data``
  attribute, to refresh the access token just do::

    from social_auth.backends.reddit import RedditAuth

    user = User.objects.get(pk=foo)
    social = user.social_auth.filter(provider='reddit')[0]
    new_token = RedditAuth.refresh_token(social.extra_data['refresh_token'],
                                         redirect_uri='http://localhost:8000/complete/reddit/')
    s.extra_data.update(new_token)
    s.save()

  Reddit requires ``redirect_uri`` when refreshing the token and it must be the
  same value used during the auth process.

.. _Reddit Preferences Apps: https://ssl.reddit.com/prefs/apps/
.. _OAuth2 authentication workflow: https://github.com/reddit/reddit/wiki/OAuth2
