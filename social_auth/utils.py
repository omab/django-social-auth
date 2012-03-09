import urlparse
import logging
from collections import defaultdict

from django.conf import settings
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType


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
    backend_name = backend.AUTH_BACKEND.name.upper().replace('-', '_')
    return setting('%s_%s' % (backend_name, name)) or \
           setting(name) or \
           default


logger = None
if not logger:
    logging.basicConfig()
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
