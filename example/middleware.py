from django.core.urlresolvers import reverse

from social_auth.backends.exceptions import AuthAlreadyAssociated
from social_auth.middleware import SocialAuthExceptionMiddleware


class ExampleSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            return "Somebody is already using that account!"
        return "We got some splainin' to do!"

    def get_redirect_uri(self, request, exception):
        return reverse('done')
