import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'contrib',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TEST_TWITTER_USER = ""
TEST_TWITTER_PASSWORD = ""

TEST_GOOGLE_USER = ""
TEST_GOOGLE_PASSWORD = ""
