from .admin import ADMIN_URL, ADMINS, BMA_NOTIFICATIONS_URL, DASHBOARD_URL
from .app_settings import *
from .auth import AUTH_PASSWORD_VALIDATORS
from .database import DATABASES
from .defaults import *  # noqa
from .email import (
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_TIMEOUT,
    EMAIL_USE_SSL,
    EMAIL_USE_TLS,
    SERVER_EMAIL,
    WEBMAIL_CONTACT_EMAIL,
)
from .environment import (
    BMA_NOTIFICATIONS_ACCOUNT,
    DEBUG,
    DOMAIN_NAME,
    GIT_HASH,
    SECRET_KEY,
    SITE_NAME,
)
from .google import GOOGLE_RECAPTCHA_SECRET
from .installed_apps import INSTALLED_APPS
from .internationalization import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .logging import LOGGING
from .media import MEDIA_ROOT, MEDIA_URL
from .middleware import MIDDLEWARE
from .staticfiles import STATIC_ROOT, STATIC_URL, STATICFILES_DIRS
from .templates import TEMPLATES

# Core setup
SITE_ID = 4
WSGI_APPLICATION = "beatonma.wsgi.application"


ALLOWED_HOSTS = [
    DOMAIN_NAME,
    "localhost",
    "django",
    "nginx-server-tests",
]
CSRF_TRUSTED_ORIGINS = [
    f"https://{DOMAIN_NAME}",
    "http://localhost",
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

TEST_RUNNER = "basetest.testrunner.PytestTestRunner"
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/"
