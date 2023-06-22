"""Views that help us ensure that things are working as they should."""

from celery.utils.log import get_logger
from dashboard.tasks.check_celery import check_celery_works
from dashboard.views.dashboard import StaffView
from django.http import HttpResponse

log = get_logger(__name__)


class CeleryTaskTestView(StaffView):
    def get(self, request, *args, **kwargs):
        params = {**request.GET}
        result = check_celery_works(**params)

        status_code = 200 if result.success else 400
        return HttpResponse(
            status=status_code,
            content=result.message,
            content_type="text/plain",
        )
