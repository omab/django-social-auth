from django.conf import settings
from social.strategies.utils import get_strategy
from social.apps.django_app.utils import BACKENDS, STORAGE
from social.utils import setting_name


STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'social_auth.strategy.DSAStrategy')


def load_strategy(*args, **kwargs):
    return get_strategy(BACKENDS, STRATEGY, STORAGE, *args, **kwargs)
