import logging
import time
from dataclasses import dataclass
from typing import Optional

from celery import shared_task
from dashboard.models.celery_task_test import CeleryTaskTest
from django.utils import timezone

log = logging.getLogger(__name__)


@shared_task
def sample_celery_task(name: str, **kwargs):
    log.info(f"sample_celery_task ran with kwargs: {kwargs}")
    CeleryTaskTest.objects.create(name=name)


@dataclass
class SampleCeleryTaskResult:
    success: bool
    message: str


def check_celery_works(name: Optional[str] = None, **params) -> SampleCeleryTaskResult:
    if not name:
        name = timezone.now().strftime("%Y%m%d-%H%M%S")

    sample_celery_task.delay(name, **params)

    # Poll CeleryTaskTest objects until the object is created
    for n in range(10):
        try:
            obj = CeleryTaskTest.objects.get()
            msg = f"Celery successfully created object '{obj}'!"
            log.info(msg)
            obj.delete()
            return SampleCeleryTaskResult(True, msg)

        except CeleryTaskTest.DoesNotExist:
            log.debug(f"CeleryTaskTest(name={name}) not created yet (n={n})")
            time.sleep(0.5)

    msg = f"Object (name={name}) was not created - check your celery configuration!"
    log.warning(msg)

    return SampleCeleryTaskResult(False, msg)
