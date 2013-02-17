Miscellaneous
=============

Mailing list
------------

Join to `django-social-auth discussion list`_ and bring any questions or suggestions
that would improve this application.


Custom User model
-----------------

If defining a custom user model, do not import ``social_auth`` from any
``models.py`` that would finally import from the ``models.py`` that defines
your ``User`` class or it will make your project fail with a recursive import
because ``social_auth`` uses ``get_model()`` to retrieve your User.


Third party backends
--------------------

There's an ongoing movement to create a list of third party backends on
djangopackages.com_, so, if somebody doesn't want its backend in the
``contrib`` directory but still wants to share, just split it in a separated
package and link it there.


Python 2.7.2rev4, 2.7.3 and Facebook backend
--------------------------------------------

It seems that this bug described in StackOverflow_ hits users using
django-social-auth_ with Python versions 2.7.2rev4 and 2.7.3 (so far) and
Facebook backend. The bug report `#315`_ explains it a bit more and shows
a workaround fit to avoid it.


Server date time
----------------

A bad date in the server might cause errors in the auth process on some services
like Twitter (probably all OAuth1.0 since timestamp is passed in the parameters
to request a token).

This issue is usually solved by installing ``ntp`` in the server (which is
a good practice to have too), and syncing the time with some ntp pool service.


url Template Tag
----------------

Since Django 1.3 the URL templatetag ``{% url socialauth_begin ... %}`` syntax
is deprecated in favor the new format where the URL name is quoted (using
single quotes). See the `release notes`_ for details.

The new syntax is not enforced yet but will be on Django 1.5, and it's also
available by importing ``url`` tag from ``future`` module doing::

    {% load url from future %}

In case of experiencing issues similar to `#303`_, check the tag being used and
its syntax.


Heroku and SSL
--------------

Seems that Heroku fails to pass the needed headers to indicate that the app is
behind SSL, this causes troubles when building the redirect URLs used in the
authentication process and providers respond with invalid redirect URL error.
To enforce ``https://`` when building the URLs just define this setting::

    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

.. _South: http://south.aeracode.org/
.. _django-social-auth: https://github.com/omab/django-social-auth
.. _djangopackages.com: http://djangopackages.com/grids/g/social-auth-backends/
.. _django-social-auth discussion list: https://groups.google.com/group/django-social-auth
.. _StackOverflow: http://stackoverflow.com/questions/9835506/urllib-urlopen-works-on-sslv3-urls-with-python-2-6-6-on-1-machine-but-not-wit
.. _#315: https://github.com/omab/django-social-auth/issues/315
.. _release notes: https://docs.djangoproject.com/en/1.3/releases/1.3/#changes-to-url-and-ssi
.. _#303: https://github.com/omab/django-social-auth/issues/303
