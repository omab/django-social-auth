from django.conf import settings


if getattr(settings, 'FACEBOOK_APP_AUTH', False):
    from social.backends.facebook import \
            FacebookAppOAuth2 as FacebookBackendBase
else:
    from social.backends.facebook import FacebookOAuth2 as FacebookBackendBase


REDIRECT_HTML = """
<script type="text/javascript">
    var domain = 'https://apps.facebook.com/',
        redirectURI = domain + '{{ FACEBOOK_APP_NAMESPACE }}' + '/';
    window.top.location = 'https://www.facebook.com/dialog/oauth/' +
    '?client_id={{ FACEBOOK_KEY }}' +
    '&redirect_uri=' + encodeURIComponent(redirectURI) +
    '&scope={{ FACEBOOK_EXTENDED_PERMISSIONS }}';
</script>
"""


class FacebookBackend(FacebookBackendBase):
    def auth_html(self):
        key, secret = self.get_key_and_secret()
        namespace = self.setting('NAMESPACE', None)
        scope = self.get_scope()
        if scope:
            scope = self.SCOPE_SEPARATOR.join(scope)
        ctx = {
            'FACEBOOK_APP_NAMESPACE': namespace or key,
            'FACEBOOK_KEY': key,
            'FACEBOOK_EXTENDED_PERMISSIONS': scope,
            'FACEBOOK_COMPLETE_URI': self.redirect_uri,
        }
        tpl = self.setting('LOCAL_HTML', 'facebook.html')
        return self.strategy.render_html(tpl=tpl, html=REDIRECT_HTML,
                                         context=ctx)
