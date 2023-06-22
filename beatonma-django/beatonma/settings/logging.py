import logging
import os

from .environment import DJANGO_LOGGING_DIR

default_loglevel = logging.INFO

_log_apps = [
    # Internal
    "bma_dev",
    "bma_app",
    "common",
    "contact",
    "dashboard",
    "github",
    "main",
    # External/peripheral
    "bmanotify_django",
    "mentions",
    "webmentions_tester",
    # 3rd party
    "django",
    "celery",
    "celery.task",
]


def _file_handler(name: str, level=default_loglevel) -> dict:
    filepath = os.path.join(DJANGO_LOGGING_DIR, f"{name.replace('.', '-')}.log")
    return {
        "level": level,
        "class": "logging.handlers.RotatingFileHandler",
        "formatter": "verbose",
        "filename": filepath,
        "maxBytes": 1 * 1024 * 1024,
        "backupCount": 2,
    }


def _logger(*handlers: str, level=default_loglevel) -> dict:
    return {
        "handlers": [*handlers, "file", "console", "mail_admins"],
        "level": level,
    }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "file": _file_handler("beatonma"),
        **{f"file_{app}": _file_handler(app) for app in _log_apps},
        "console": {
            "level": default_loglevel,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": logging.ERROR,
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {f"{app}": _logger(f"file_{app}") for app in _log_apps},
}
