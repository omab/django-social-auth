from setuptools import setup, find_packages

setup(
    name='django-social-auth',
    version="1.0",
    author='Matias Aguirre',
    author_email='matiasaguirre@gmail.com',
    url='https://github.com/omab/django-social-auth',
    install_requires=['django', 'python-openid', 'oauth'],
    description = 'Django social authentication made simple.',
    packages=find_packages(),
    include_package_data=True,
)