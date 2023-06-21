import logging

from contact.models.webmailmessage import WebmailMessage
from contact.tasks import send_email
from django.http import HttpResponse
from main.views.decorators import RecaptchaView

log = logging.getLogger(__name__)


class ContactApiView(RecaptchaView):
    def post(self, request, *args, **kwargs):
        message = WebmailMessage.create_from_http_post(request.POST)
        log.info(f"Queuing webmail from '{message.name}' (id={message.pk})...")

        send_email(request.POST)

        return HttpResponse(status=202)
