from common.util.client import get_client_ip
from common.views.api import ApiView
from django.http import JsonResponse
from django_user_agents.utils import get_user_agent


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
