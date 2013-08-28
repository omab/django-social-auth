Use Cases
=========

Some particular use cases are listed below.

Account association only
------------------------

Check the documentation about `Pipelines <pipeline.html>`_ for an example of
single association, since association URLs are deprecated.


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


Combining associate_user and load_extra_data functions in the pipeline
----------------------------------------------------------------------

Two functions under backends.pipeline.social module, ``associate_user`` and
``load_extra_data`` are commonly used back to back in the ``SOCIAL_AUTH_PIPELINE``.
Both of these modules hit the database for associating the social_user and 
loading extra data for this social_user. If you want to combine these two functions
in order to decrease number of database visits, you can use this function::

    def social_associate_and_load_data(backend, details, response, uid, user,
                                       social_user=None, *args, **kwargs):
        """
        The combination of associate_user and load_extra_data functions
        of django-social-auth. The reason for combining these two pipeline
        functions is decreasing the number of database visits.
        """
        extra_data = backend.extra_data(user, uid, response, details)
        created = False
        if not social_user and user:
            social_user, created = UserSocialAuth.objects.get_or_create(
                user_id=user.id,
                provider=backend.name,
                uid=uid,
                defaults={'extra_data': extra_data})

        if not created and extra_data and social_user.extra_data != extra_data:
            social_user.extra_data.update(extra_data)
            social_user.save()
        return {'social_user': social_user}
