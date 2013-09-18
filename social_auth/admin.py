from django.conf import settings


MODELS = getattr(settings, 'SOCIAL_AUTH_MODELS',
                 'social_auth.db.django_models')


if MODELS == 'social_auth.db.django_models':
    from social.apps.django_app.default import admin
    admin  # placate pyflakes
