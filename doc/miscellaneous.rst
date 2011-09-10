Miscellaneous
=============

Join to django-social-auth_ community on Convore_ and bring any questions or
suggestions that will improve this app.


South_ users should add this rule to enable migrations::

    try:
        import south
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], ["^social_auth\.fields\.JSONField"])
    except:
        pass

If defining a custom user model, do not import social_auth from any models.py
that would finally import from the models.py that defines your User class or it
will make your project fail with a recursive import because social_auth uses
get_model() to retrieve your User.

There's an ongoing movement to create a list of third party backends on
djangopackages.com_, so, if somebody doesn't want it's backend in the
``contrib`` directory but still wants to share, just split it in a separated
package and link it there.


.. _South: http://south.aeracode.org/
.. _django-social-auth: https://convore.com/django-social-auth/
.. _Convore: https://convore.com/
.. _djangoproject.com: http://djangopackages.com/grids/g/social-auth-backends/
