import logging

from django.http import HttpResponse

from common.views.logged import LoggedView

log = logging.getLogger(__name__)


class PingView(LoggedView):
    """Return a simple response to confirm the server is available."""

    def get(self, request, *args, **kwargs):
        return HttpResponse("OK", status=200)
