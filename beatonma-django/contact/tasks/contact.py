import logging

from bmanotify_django.tasks import dispatch_fcm_notification
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from django.http import QueryDict
from main.views.decorators import recaptcha

django_log = logging.getLogger(__name__)
task_log = get_task_logger(f"{__name__}.tasks")


def send_email(http_post: QueryDict):
    name = http_post.get("name", "No name given")
    contact = http_post.get("contact_method", "No contact info given")
    subject = http_post.get("subject", "beatonma.org webmail")
    message_body = http_post.get("message", "No message given")
    tags = http_post.get("tags", "beatonma.org,important")
    color = http_post.get("color", "#ff4081")

    if getattr(settings, "CELERY_DISABLED", False):
        django_log.warning(
            f"[send_email | celery is disabled] name='{name}', "
            f"contact='{contact}', message_body='{message_body}"
        )
        return

    try:
        _send_email.delay(
            http_post=http_post,
            name=name,
            contact=contact,
            subject=subject,
            message_body=message_body,
            tags=tags,
            color=color,
        )
    except Exception as e:
        django_log.error(f"send_email error: {e}")


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
@recaptcha
def _send_email(
    http_post: QueryDict,  # noqa Required for @recaptcha
    name: str,
    contact: str,
    subject: str,
    message_body: str,
    tags: str,
    color: str,
):
    message = (
        f"Name: '{name}'\n"
        f"Contact info: '{contact}'\n\n"
        f"Subject: '{subject}'\n"
        f"Message:"
        f"\n```\n"
        f"{message_body}\n"
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
        f"From '{name}': {message_body}",
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
