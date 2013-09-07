import warnings

from social.backends.vk import VKontakteOpenAPI as VKOpenAPIBackend, \
                               VKOAuth2 as VKOAuth2Backend, \
                               VKAppOAuth2 as VKApplicationBackend

warnings.warn('Vkontakte backend was renamed to vk backend, '
              'settings were renamed too. Please adjust your '
              'settings', DeprecationWarning)
