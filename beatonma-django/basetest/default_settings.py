from beatonma.settings import *  # noqa

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

# Remote services
FCM_PROJECT_ID = "fake-project-id"
FCM_SERVICE_ACCOUNT_FILE = "fake-file.json"
GITHUB_ACCESS_TOKEN = "fake-github-token"
GITHUB_USERNAME = "beatonma"
GOOGLE_RECAPTCHA_SECRET = "fake-recaptcha-secret"
SENTRY_ENABLED = False

SITE_NAME = "test"
ADMIN_URL = "admin/"
BMA_NOTIFICATIONS_URL = "notifications/"

MEDIA_ROOT = "/tmp/bma-tests/media/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.DEBUG,
        },
    },
    "loggers": {
        app: {
            "level": logging.DEBUG,
            "handlers": ["console"],
        }
        for app in INSTALLED_APPS
    },
}
