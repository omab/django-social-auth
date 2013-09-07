from social_auth import IS_DJANGO_MODELS


if IS_DJANGO_MODELS:
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
