"""Admin settings"""
from django.contrib import admin

from .models import UserSocialAuth, Nonce, Association


class UserSocialAuthOption(admin.ModelAdmin):
    """Social Auth user options"""
    list_display = ('id', 'user', 'provider')
    search_fields = ('user__name',)
    list_filter = ('provider',)
    raw_id_fields = ('user',)


class NonceOption(admin.ModelAdmin):
    """Nonce options"""
    list_display = ('id', 'server_url', 'timestamp', 'salt')


class AssociationOption(admin.ModelAdmin):
    """Association options"""
    list_display = ('id', 'server_url', 'assoc_type')
    list_filter = ('assoc_type',)


admin.site.register(UserSocialAuth, UserSocialAuthOption)
admin.site.register(Nonce, NonceOption)
admin.site.register(Association, AssociationOption)
