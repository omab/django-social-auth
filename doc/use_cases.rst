Use Cases
=========

Some particular use cases are listed below.

Account association only
------------------------

Use social auth just for account association (no login)::

    from django.contrib.auth.decorators import login_required

    from social_auth.views import auth, complete, disconnect

    urlpatterns += patterns('',
        url(r'^associate/(?P<backend>[^/]+)/$',
            login_required(auth),
            name='socialauth_begin'),
        url(r'^associate/complete/(?P<backend>[^/]+)/$',
            login_required(complete),
            name='socialauth_complete'),

        url(r'^disconnect/(?P<backend>[^/]+)/$',
            disconnect,
            name='socialauth_disconnect'),
        url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
            disconnect,
            name='socialauth_disconnect_individual'),
    )


Client side authorization libraries
-----------------------------------

OAuth providers like Facebook provide some form of Javascript library/SDK to
perform client side authorization. That authorization can be stored using
django-social-auth by defining a simple view like this::

    from django.contrib.auth import login
    from django.shortcuts import redirect
    from social_auth.decorators import dsa_view

    @dsa_view()
    def register_by_access_token(request, backend, *args, **kwargs):
        access_token = request.GET.get('access_token')
        user = backend.do_auth(access_token)
        if user and user.is_active:
            login(request, user)
        return redirect('/')

This view just expects the ``access_token`` as a GET parameter and the backend
name in the URL (check django-social-auth URLs).


Token refreshing
----------------

OAuth2 defines a mechanism to refresh the ``access_token`` once it expires.
Not all the providers support it, and some providers implement it in some way
or another. Usually there's a ``refresh_token`` involved (a token that
identifies the user but it's only used to retrieve a new ``access_token``).

To refresh the token on a given social account just call the
``refresh_token()`` in the ``UserSocialAuth`` instance, like this::

    user = User.objects.get(...)
    social = user.social_auth.filter(provider='google-oauth2')[0]
    social.refresh_token()

At the moment just a few backends were tested against token refreshing
(Google OAuth2, Facebook and Stripe). Other backends probably also support
it (if they follow the OAuth2 standard) with the default mechanism. Others
don't support it because the token is not supposed to expire.
