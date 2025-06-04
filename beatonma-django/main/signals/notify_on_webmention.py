from contact.tasks import send_notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from mentions.models import Webmention


@receiver(post_save, sender=Webmention, dispatch_uid="notify_on_new_webmention")
def notify_on_new_webmention(sender, instance: Webmention, created: bool, **kwargs):
    if created:
        send_notification(
            title="Webmention",
            body=f"To: {instance.target_url}\nFrom: {instance.source_url}",
        )
