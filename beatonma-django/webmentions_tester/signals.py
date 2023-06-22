import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from mentions.models import OutgoingWebmentionStatus

from webmentions_tester.models import TemporaryMention

log = logging.getLogger(__name__)


@receiver(
    post_save,
    sender=OutgoingWebmentionStatus,
    dispatch_uid="update_temp_mention_when_outgoing_status_created",
)
def update_temp_mention_when_outgoing_status_created(
    sender,
    instance: OutgoingWebmentionStatus,
    **kwargs,
):
    if not instance.status_message:
        return

    temp = (
        TemporaryMention.objects.filter(
            url=instance.target_url, outgoing_status__isnull=True
        )
        .order_by("-submission_time")
        .first()
    )

    if temp:
        temp.outgoing_status = instance
        temp.save()
        log.info(f"Updated TemporaryMention via signal: {temp}")

    else:
        log.warning(f"TemporaryMention not found for url={instance.target_url}")
