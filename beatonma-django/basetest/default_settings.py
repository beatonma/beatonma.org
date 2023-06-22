import logging
import uuid
from pathlib import Path

from beatonma.settings.installed_apps import INSTALLED_APPS  # noqa
from beatonma.settings.middleware import MIDDLEWARE  # noqa
from beatonma.settings.templates import TEMPLATES  # noqa

BASE_DIR = Path(__file__).parent.parent

ALLOWED_HOSTS = ["localhost"]
SITE_ID = 1
ROOT_URLCONF = "beatonma.urls"

SECRET_KEY = "some-test-key"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "temp.db"}}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "/static/"

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

TEST_API_KEY = uuid.uuid4().hex
HTTP_REQUEST_HEADERS = {}

ADMINS = []

CELERY_BROKER_URL = "fake-celery-broker-url"

# Taggit - tag manager
TAGGIT_CASE_INSENSITIVE = True

# Remote services
FCM_API_KEY = "fake-fcm-key"
GITHUB_ACCESS_TOKEN = "fake-github-token"
GITHUB_USERNAME = "beatonma"
GOOGLE_RECAPTCHA_SECRET = "fake-recaptcha-secret"
SENTRY_ENABLED = False

SITE_NAME = "test"
ADMIN_URL = "admin/"
DASHBOARD_URL = "dashboard/"
BMA_NOTIFICATIONS_URL = "notifications/"

MEDIA_ROOT = "/tmp/bma-tests/media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.DEBUG,
        },
    },
    "loggers": {
        app: {
            "level": logging.WARNING,
            "handlers": ["console"],
        }
        for app in [
            "bma_app",
            "bma_dev",
            "common",
            "contact",
            "dashboard",
            "django",
            "github",
            "main",
            "webmentions_tester",
        ]
    },
}
