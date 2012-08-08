import time
import random
import hashlib
import urlparse
import urllib
from urllib2 import urlopen
import logging

from collections import defaultdict
from datetime import timedelta, tzinfo

from django.conf import settings
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import SimpleLazyObject


try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


try:
    from django.utils.crypto import get_random_string as random_string
except ImportError:  # django < 1.4
    # Implementation borrowed from django 1.4
    def random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        if not using_sysrandom:
            random.seed(hashlib.sha256('%s%s%s' % (random.getstate(),
                                                   time.time(),
                                                   settings.SECRET_KEY))
                               .digest())
        return ''.join([random.choice(allowed_chars) for i in range(length)])


try:
    from django.utils.timezone import utc as django_utc
except ImportError:  # django < 1.4
    class UTC(tzinfo):
        """UTC implementation taken from django 1.4."""
        def __repr__(self):
            return '<UTC>'

        def utcoffset(self, dt):
            return timedelta(0)

        def tzname(self, dt):
            return 'UTC'

        def dst(self, dt):
            return timedelta(0)

    django_utc = UTC()


try:
    from django.utils.crypto import constant_time_compare as ct_compare
except ImportError:  # django < 1.4
    def ct_compare(val1, val2):
        if len(val1) != len(val2):
            return False
        result = 0
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)
        return result == 0


try:
    from django.utils.functional import empty
except ImportError:  # django < 1.4
    empty = None


get_random_string = random_string
constant_time_compare = ct_compare
utc = django_utc


def sanitize_log_data(secret, data=None, leave_characters=4):
    """
    Clean private/secret data from log statements and other data.

    Assumes data and secret are strings. Replaces all but the first
    `leave_characters` of `secret`, as found in `data`, with '*'.

    If no data is given, all but the first `leave_characters` of secret
    are simply replaced and returned.
    """
    replace_secret = (secret[:leave_characters] +
                      (len(secret) - leave_characters) * '*')

    if data:
        return data.replace(secret, replace_secret)

    return replace_secret


def sanitize_redirect(host, redirect_to):
    """
    Given the hostname and an untrusted URL to redirect to,
    this method tests it to make sure it isn't garbage/harmful
    and returns it, else returns None, similar as how's it done
    on django.contrib.auth.views.

    >>> print sanitize_redirect('myapp.com', None)
    None
    >>> print sanitize_redirect('myapp.com', '')
    None
    >>> print sanitize_redirect('myapp.com', {})
    None
    >>> print sanitize_redirect('myapp.com', 'http://notmyapp.com/path/')
    None
    >>> print sanitize_redirect('myapp.com', 'http://myapp.com/path/')
    http://myapp.com/path/
    >>> print sanitize_redirect('myapp.com', '/path/')
    /path/
    """
    # Quick sanity check.
    if not redirect_to:
        return None

    # Heavier security check, don't allow redirection to a different host.
    try:
        netloc = urlparse.urlparse(redirect_to)[1]
    except TypeError:  # not valid redirect_to value
        return None

    if netloc and netloc != host:
        return None

    return redirect_to


def group_backend_by_type(items, key=lambda x: x):
    """Group items by backend type."""

    # Beware of cyclical imports!
    from social_auth.backends import \
        get_backends, OpenIdAuth, BaseOAuth, BaseOAuth2

    result = defaultdict(list)
    backends = get_backends()

    for item in items:
        backend = backends[key(item)]
        if issubclass(backend, OpenIdAuth):
            result['openid'].append(item)
        elif issubclass(backend, BaseOAuth2):
            result['oauth2'].append(item)
        elif issubclass(backend, BaseOAuth):
            result['oauth'].append(item)
    return dict(result)


def setting(name, default=None):
    """Return setting value for given name or default value."""
    return getattr(settings, name, default)


def backend_setting(backend, name, default=None):
    """
    Looks for setting value following these rules:
        1. Search for <backend_name> prefixed setting
        2. Search for setting given by name
        3. Return default
    """
    backend_setting_name = '{0}_{1}'.format(
        backend.AUTH_BACKEND.name.upper().replace('-', '_'),
        name
    )
    if hasattr(settings, backend_setting_name):
        return setting(backend_setting_name)
    elif hasattr(settings, name):
        return setting(name)
    else:
        return default


logger = None
if not logger:
    logger = logging.getLogger('SocialAuth')
    logger.setLevel(logging.DEBUG)


def log(level, *args, **kwargs):
    """Small wrapper around logger functions."""
    {'debug': logger.debug,
     'error': logger.error,
     'exception': logger.exception,
     'warn': logger.warn}[level](*args, **kwargs)


def model_to_ctype(val):
    """Converts values that are instance of Model to a dictionary
    with enough information to retrieve the instance back later."""
    if isinstance(val, Model):
        val = {
            'pk': val.pk,
            'ctype': ContentType.objects.get_for_model(val).pk
        }
    return val


def ctype_to_model(val):
    """Converts back the instance saved by model_to_ctype function."""
    if isinstance(val, dict) and 'pk' in val and 'ctype' in val:
        ctype = ContentType.objects.get_for_id(val['ctype'])
        ModelClass = ctype.model_class()
        val = ModelClass.objects.get(pk=val['pk'])
    return val


def clean_partial_pipeline(request):
    """Cleans any data for partial pipeline."""
    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    # Check for key to avoid flagging the session as modified unnecessary
    if name in request.session:
        request.session.pop(name, None)


def log_exceptions_to_messages(request, backend, err):
    """Log exception messages to messages app if it's installed."""
    if 'django.contrib.messages' in setting('INSTALLED_APPS'):
        from django.contrib.messages.api import error
        name = backend.AUTH_BACKEND.name
        error(request, unicode(err), extra_tags='social-auth %s' % name)


def url_add_parameters(url, params):
    """Adds parameters to URL, parameter will be repeated if already present"""
    if params:
        fragments = list(urlparse.urlparse(url))
        fragments[4] = urllib.urlencode(urlparse.parse_qsl(fragments[4]) +
                                        params.items())
        url = urlparse.urlunparse(fragments)
    return url


class LazyDict(SimpleLazyObject):
    """Lazy dict initialization."""
    def __getitem__(self, name):
        if self._wrapped is empty:
            self._setup()
        return self._wrapped[name]

    def __setitem__(self, name, value):
        if self._wrapped is empty:
            self._setup()
        self._wrapped[name] = value


def dsa_urlopen(*args, **kwargs):
    """Like urllib2.urlopen but sets a timeout defined by
    SOCIAL_AUTH_URLOPEN_TIMEOUT setting if defined (and not already in
    kwargs)."""
    timeout = setting('SOCIAL_AUTH_URLOPEN_TIMEOUT')
    if timeout and 'timeout' not in kwargs:
        kwargs['timeout'] = timeout
    return urlopen(*args, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
