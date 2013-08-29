# TODO: review HTML rendering in facebook app backend
if getattr(settings, 'FACEBOOK_APP_AUTH', False):
    from social.backends.facebook import FacebookAppOAuth2 as FacebookBackend
else:
    from social.backends.facebook import FacebookOAuth2 as FacebookBackend
