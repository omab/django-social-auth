from django.conf import settings


if getattr(settings, 'EVERNOTE_DEBUG', False):
    from social.backends.evernote import EvernoteSandboxOAuth as EvernoteAuth
else:
    from social.backends.evernote import EvernoteOAuth as EvernoteAuth
