import urlparse
from collections import defaultdict

from social_auth.backends import BACKENDS, OpenIdAuth, BaseOAuth, BaseOAuth2


def sanitize_redirect(host, redirect_to):
    """
    Given the hostname and an untrusted URL to redirect to,
    this method tests it to make sure it isn't garbage/harmful
    and returns it, else returns None.

    See http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/views.py#L36

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
    result = defaultdict(list)

    for item in items:
        backend = BACKENDS[key(item)]
        if issubclass(backend, OpenIdAuth):
            result['openid'].append(item)
        elif issubclass(backend, BaseOAuth2):
            result['oauth2'].append(item)
        elif issubclass(backend, BaseOAuth):
            result['oauth'].append(item)
    return dict(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
