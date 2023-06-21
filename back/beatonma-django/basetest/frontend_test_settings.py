from .default_settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "frontend-tests.sqlite3",
    }
}

# https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha.-what-should-i-do
GOOGLE_RECAPTCHA_SECRET = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

DEBUG = True
CELERY_DISABLED = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8123",
]

STATIC_ROOT = "/tmp/bma-tests/static/"
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    BASE_DIR / "main/static/main/",
    BASE_DIR / "dashboard/static/dashboard/",
    BASE_DIR / "webapp/static/",
)
