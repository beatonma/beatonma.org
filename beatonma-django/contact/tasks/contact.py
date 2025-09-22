import logging
import traceback

from bmanotify_django.tasks import dispatch_fcm_notification
from bmanotify_django.tasks.dispatch import NoRegisteredDevice
from celery import shared_task
from celery.utils.log import get_task_logger
from common.util.tasks import dispatch_task
from django.conf import settings
from django.core.mail import send_mail

django_log = logging.getLogger(__name__)
task_log = get_task_logger(f"{__name__}.tasks")


def log(level, message):
    django_log.log(level, message)
    task_log.log(level, message)


def send_notification(
    title: str,
    body: str,
    tags: str = settings.SITE_NAME,
    color: str = "#ff4081",
    important: bool = False,
):
    try:
        dispatch_task(
            _send_notification,
            title=title,
            body=body,
            tags=tags,
            color=color,
            important=important,
        )
    except Exception as e:
        log(logging.ERROR, f"send_notification error: {e}")


def send_error(title: str, exception: BaseException):
    formatted_error = f"""{str(exception)}\n{traceback.format_exception(exception)}"""
    log(logging.ERROR, formatted_error)
    send_notification(
        title,
        body=formatted_error,
        color="#C70036",
        important=True,
    )


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

    log(logging.INFO, f"Sending mail from: '{name}'")

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.WEBMAIL_CONTACT_EMAIL],
    )

    try:
        _send_notification(
            subject,
            f"From '{name}': {message}",
            tags=tags,
            color=color,
            important=True,
        )
    except NoRegisteredDevice:
        log(
            logging.WARNING,
            "Could not send notification because no devices are registered",
        )

    log(logging.INFO, f"Mail sent from '{name}'")


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
