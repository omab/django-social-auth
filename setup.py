# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup


setup(name='django-social-auth',
      version='0.1',
      author='Matías Aguirre',
      author_email='matiasaguirre@gmail.com',
      description='Django social authentication made simple.',
      license='GPL',
      keywords='django, openid, oath, social auth, application',
      url='https://github.com/omab/django-social-auth',
      packages=['social_auth'],
      long_description=open(join(dirname(__file__), 'README.rst')).read(),
      requires=['django (>=1.2)',
                'oauth (>=1.0)',
                'python_openid (>=2.2)'],
      classifiers=['Framework :: Django',
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python'])
