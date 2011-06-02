
Installation
============

------------
Dependencies
------------
Dependencies that **must** be meet to use the application:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on python-oauth2_

- Several backends demands application registration on their corresponding
  sites.


----------
Get a copy
----------

From pypi_::

    $ pip install django-social-auth

or::

    $ easy_install django-social-auth

or clone from github_::

    $ git clone git://github.com/omab/django-social-auth.git

and add social_auth to PYTHONPATH::

    $ export PYTHONPATH=$PYTHONPATH:$(pwd)/django-social-auth/

or::

    $ cd django-social-auth
    $ sudo python setup.py install


.. _OpenId: http://openid.net/
.. _OAuth: http://oauth.net/
.. _pypi: http://pypi.python.org/pypi/django-social-auth/
.. _github: https://github.com/omab/django-social-auth
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _python-oauth2: https://github.com/simplegeo/python-oauth2
