# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup


version = __import__('social_auth').__version__

LONG_DESCRIPTION = """
Django Social Auth is an easy to setup social authentication/registration
mechanism for Django projects.

Crafted using base code from django-twitter-oauth_ and django-openid-auth_,
implements a common interface to define new authentication providers from
third parties.
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


setup(name='django-social-auth',
      version=version,
      author='Matías Aguirre',
      author_email='matiasaguirre@gmail.com',
      description='Django social authentication made simple.',
      license='BSD',
      keywords='django, openid, oauth, social auth, application',
      url='https://github.com/omab/django-social-auth',
      packages=['social_auth',
                'social_auth.backends',
                'social_auth.backends.contrib',
                'social_auth.backends.pipeline',
                'social_auth.db'],
      package_data={'social_auth': ['locale/*/LC_MESSAGES/*']},
      long_description=long_description(),
      install_requires=['django>=1.2.5',
                        'oauth2>=1.5.167',
                        'python_openid>=2.2'],
      classifiers=['Framework :: Django',
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7'])
