import urlparse

def sanitize_redirect(host, redirect_to):
    """
    Given the hostname and an untrusted URL to redirect to,
    this method tests it to make sure it isn't garbage/harmful
    and returns it, else returns None.

    See http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/views.py#L36
    """
    # Quick sanity check.
    if not redirect_to:
        return None
    netloc = urlparse.urlparse(redirect_to)[1]
    # Heavier security check -- don't allow redirection to a different host.
    if netloc and netloc != host:
        return None
    return redirect_to
