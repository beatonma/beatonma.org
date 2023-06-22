import logging
import os
import sys
from typing import Optional

log = logging.getLogger(__name__)

__TESTING = "test" in sys.argv


def _env_str(key: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(key, default)
    if value is None and not __TESTING and default is not None:
        log.warning(f"No value for environment.{key}")
    return value


def _env_bool(key: str, default: bool) -> bool:
    return _env_str(key, str(default)).lower() == "true"


def _env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    try:
        return int(_env_str(key, str(default)))
    except ValueError:
        if not __TESTING:
            log.error(f"Expected int value for environment key '{key}'")


# Core
DEBUG: bool = _env_bool("DEBUG", default=False)
DOMAIN_NAME: str = _env_str("DOMAIN_NAME")
SITE_NAME: str = _env_str("SITE_NAME")
SECRET_KEY: str = _env_str("SECRET_KEY")
DJANGO_LOGGING_DIR: str = _env_str("DJANGO_LOGGING_DIR", default="/var/log/beatonma/")
GIT_HASH: str = _env_str("GIT_HASH")

# Database
POSTGRES_DB: str = _env_str("POSTGRES_DB")
POSTGRES_USER: str = _env_str("POSTGRES_USER")
POSTGRES_PASSWORD: str = _env_str("POSTGRES_PASSWORD")
POSTGRES_HOST: str = _env_str("POSTGRES_HOST")
POSTGRES_PORT: int = _env_int("POSTGRES_PORT", 5432)

# URLs
ADMIN_URL: str = _env_str("ADMIN_URL")
DASHBOARD_URL: str = _env_str("DASHBOARD_URL")
BMA_NOTIFICATIONS_URL: str = _env_str("BMA_NOTIFICATIONS_URL")

# File paths
MEDIA_ROOT: str = _env_str("MEDIA_ROOT", default="/var/www/media")
STATIC_ROOT: str = _env_str("STATIC_ROOT", default="/var/www/static")
TEMPLATE_ROOT: str = _env_str("TEMPLATE_ROOT", default=None)
STATICFILES_ROOT: str = _env_str("STATICFILES_ROOT", default=None)

# Email
SERVER_EMAIL: str = _env_str("SERVER_EMAIL")
EMAIL_HOST: str = _env_str("EMAIL_HOST")
EMAIL_PORT: int = _env_int("EMAIL_PORT")
EMAIL_HOST_USER: str = _env_str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD: str = _env_str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS: bool = _env_bool("EMAIL_USE_TSL", True)
EMAIL_USE_SSL: bool = _env_bool("EMAIL_USE_SSL", False)
ADMIN_NAME: str = _env_str("ADMIN_NAME")
ADMIN_EMAIL: str = _env_str("ADMIN_EMAIL")

# Apps
CELERY_BROKER_URL: str = _env_str("CELERY_BROKER_URL")
GITHUB_ACCESS_TOKEN: str = _env_str("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME: str = _env_str("GITHUB_USERNAME")
SENTRY_ENABLED: bool = _env_bool("SENTRY_ENABLED", default=not DEBUG)
SENTRY_DSN: str = _env_str("SENTRY_DSN")
FCM_API_KEY: str = _env_str("FCM_API_KEY")
GOOGLE_RECAPTCHA_SECRET: str = _env_str("GOOGLE_RECAPTCHA_SECRET")
WEBMAIL_CONTACT_EMAIL: str = _env_str("WEBMAIL_CONTACT_EMAIL")
BMA_NOTIFICATIONS_ACCOUNT: str = _env_str("BMA_NOTIFICATIONS_ACCOUNT")
