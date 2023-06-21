from celery import shared_task
from celery.utils.log import get_logger
from django.http import HttpResponse

from common.views.logged import LoggedView

log = get_logger(__name__)


@shared_task
def sample_celery_task(**kwargs):
    log.info(f"sample_celery_task ran with kwargs: {kwargs}")


class CeleryTaskTestView(LoggedView):
    """Trigger a simple celery task so we can check our celery/broker configuration works."""

    def get(self, request, *args, **kwargs):
        sample_celery_task.delay(**request.GET)
        return HttpResponse(status=202)
