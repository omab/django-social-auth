from django.conf import settings

MODELS = getattr(settings, 'SOCIAL_AUTH_MODELS',
                 'social_auth.db.django_models')


if MODELS == 'social_auth.db.django_models':
    from social.apps.django_app.default.models import \
            UserSocialAuth as UserSocialAuthBase, \
            Nonce as NonceBase, \
            Association as AssociationBase, \
            DjangoStorage as DjangoStorageBase
else:
    from social.apps.django_app.me.models import \
            UserSocialAuth as UserSocialAuthBase, \
            Nonce as NonceBase, \
            Association as AssociationBase, \
            DjangoStorage as DjangoStorageBase


class UserSocialAuth(UserSocialAuthBase):
    class Meta:
        proxy = True


class Nonce(NonceBase):
    class Meta:
        proxy = True


class Association(AssociationBase):
    class Meta:
        proxy = True


class DjangoStorage(DjangoStorageBase):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
