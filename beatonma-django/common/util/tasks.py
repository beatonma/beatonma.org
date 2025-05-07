import logging
from typing import Callable

from celery.local import Proxy
from django.conf import settings

log = logging.getLogger(__name__)


def dispatch_task(task: Callable, *args, **kwargs):
    if getattr(settings, "CELERY_DISABLED", False):
        log.warning(f"Celery is disabled, running task synchronously: '{task}'")
        task(*args, **kwargs)
        return None

    task: Proxy
    return task.delay(*args, **kwargs)
