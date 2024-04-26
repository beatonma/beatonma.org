import logging

from common.util.client import get_client_ip
from common.views.api import ApiView
from common.views.logged import LoggedView
from django.http import HttpResponse, JsonResponse
from django_user_agents.utils import get_user_agent

log = logging.getLogger(__name__)


class PingView(LoggedView):
    """Return a simple response to confirm the server is available."""

    def get(self, request, *args, **kwargs):
        return HttpResponse("OK", status=200)


class WhoamiView(ApiView):
    def get(self, request):
        ua = get_user_agent(request)
        ip = get_client_ip(request)

        return JsonResponse(
            {
                "ip": ip,
                "device": ua.get_device(),
                "os": ua.get_os(),
                "browser": ua.get_browser(),
            }
        )
