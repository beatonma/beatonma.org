import logging

from bmanotify_django.tasks import dispatch_fcm_notification
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

django_log = logging.getLogger(__name__)
task_log = get_task_logger(f"{__name__}.tasks")


def send_notification(
    title: str,
    body: str,
    tags: str = settings.SITE_NAME,
    color: str = "#ff4081",
    important: bool = False,
):

    if getattr(settings, "CELERY_DISABLED", False):
        django_log.warning(
            f"[send_notification | celery is disabled] "
            f"title='{title}', body='{body}', tags='{tags}', "
            f"color='{color}', important='{important}'"
        )
        return

    try:
        _send_notification.delay(
            title=title,
            body=body,
            tags=tags,
            color=color,
            important=important,
        )
    except Exception as e:
        django_log.error(f"send_notification error: {e}")


@shared_task
def send_webmail(
    name: str,
    contact_info: str,
    message: str,
    subject: str = "beatonma webmail",
    tags: str = "beatonma.org,important",
    color: str = "#ff4081",
):
    message = (
        f"Name: '{name}'\n"
        f"Contact info: '{contact_info}'\n\n"
        f"Subject: '{subject}'\n"
        f"Message:"
        f"\n```\n"
        f"{message}\n"
        "```\n"
    )

    task_log.info(f"Sending mail from: '{name}'")

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.WEBMAIL_CONTACT_EMAIL],
    )

    _send_notification(
        subject,
        f"From '{name}': {message}",
        tags=tags,
        color=color,
        important=True,
    )

    task_log.info(f"Mail sent from '{name}'")


@shared_task
def _send_notification(
    title: str,
    body: str,
    tags: str,
    color: str,
    important: bool,
):
    sound = "important" if important else None

    dispatch_fcm_notification(
        account=settings.BMA_NOTIFICATIONS_ACCOUNT,
        message_title=title,
        message_body=body,
        tag=tags,
        color=color,
        sound=sound,
    )
