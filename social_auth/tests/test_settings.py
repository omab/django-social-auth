import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'social_auth',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TEST_TWITTER_USER = ""
TEST_TWITTER_PASSWORD = ""
