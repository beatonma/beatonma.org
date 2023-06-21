from common.models import PageView
from common.util.client import get_client_ip
from common.views import BaseView
from contact.tasks import send_notification
from django.db import Error
from django.http import HttpRequest, HttpResponse
from django_user_agents.utils import get_user_agent


class LoggedView(BaseView):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.method == "GET":
            ua = get_user_agent(request)
            ip = get_client_ip(request)
            url = request.build_absolute_uri()

            try:
                PageView.objects.create(
                    url=url[:500],
                    ip=ip,
                    ua_device=ua.get_device(),
                    ua_os=ua.get_os(),
                    ua_browser=ua.get_browser(),
                )

                if len(url) > 500:
                    raise ValueError("Suspiciously long URL")

            except (Error, ValueError) as e:
                send_notification(
                    title="beatonma.org: Suspicious request",
                    body=f"User [{ip}: {ua}] requested `{url}`\n{e}",
                    tags="beatonma.org,warning",
                    color="#ff4040",
                    important=True,
                )
                return HttpResponse(status=400)

        return super().dispatch(request, *args, **kwargs)
