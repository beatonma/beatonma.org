import logging

from beatonma.settings.app_settings import *  # noqa
from beatonma.settings.defaults import *  # noqa
from beatonma.settings.installed_apps import INSTALLED_APPS  # noqa
from beatonma.settings.internationalization import LANGUAGE_CODE  # noqa
from beatonma.settings.internationalization import TIME_ZONE  # noqa
from beatonma.settings.internationalization import USE_I18N  # noqa
from beatonma.settings.internationalization import USE_TZ  # noqa
from beatonma.settings.middleware import MIDDLEWARE  # noqa
from beatonma.settings.templates import TEMPLATES  # noqa

# Transitional setting until Django 6.0
FORMS_URLFIELD_ASSUME_HTTPS = True


ALLOWED_HOSTS = ["localhost"]
SITE_ID = 1

SECRET_KEY = "some-test-key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test.sqlite3",
    }
}

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
            "level": logging.INFO,
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
