from social_auth import IS_DJANGO_MODELS


if IS_DJANGO_MODELS:
    from social.apps.django_app.default import admin
    admin  # placate pyflakes
