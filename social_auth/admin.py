"""Admin settings"""
from social_auth.utils import setting


if setting('SOCIAL_AUTH_MODELS') in (None, 'social_auth.db.django_models'):
    from django.contrib import admin
    from social_auth.models import UserSocialAuth, Nonce, Association

    class UserSocialAuthOption(admin.ModelAdmin):
        """Social Auth user options"""
        list_display = ('id', 'user', 'provider', 'uid')
        search_fields = ('user__first_name', 'user__last_name', 'user__email',
                'user__username')
        list_filter = ('provider',)
        raw_id_fields = ('user',)
        list_select_related = True

    class NonceOption(admin.ModelAdmin):
        """Nonce options"""
        list_display = ('id', 'server_url', 'timestamp', 'salt')
        search_fields = ('server_url',)

    class AssociationOption(admin.ModelAdmin):
        """Association options"""
        list_display = ('id', 'server_url', 'assoc_type')
        list_filter = ('assoc_type',)
        search_fields = ('server_url',)

    admin.site.register(UserSocialAuth, UserSocialAuthOption)
    admin.site.register(Nonce, NonceOption)
    admin.site.register(Association, AssociationOption)
