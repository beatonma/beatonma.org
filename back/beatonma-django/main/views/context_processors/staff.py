import logging

from contact.models.webmailmessage import WebmailMessage

log = logging.getLogger(__name__)


def staff(request) -> dict:
    if not request.user.is_superuser:
        return {}

    return {
        "unread_webmail": WebmailMessage.objects.filter_unread(),
    }
