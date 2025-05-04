import logging
from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver
from github.models import GithubReleasePublishedPayload
from main.models import AppPost, ChangelogPost

log = logging.getLogger(__name__)


@receiver(
    post_save,
    sender=GithubReleasePublishedPayload,
    dispatch_uid="create_changelog_from_githubreleasepayload",
)
def create_changelog_from_githubreleasepayload(
    sender: Type,
    instance: GithubReleasePublishedPayload,
    **kwargs,
):
    repository = instance.event.repository
    if not repository.is_public():
        return

    try:
        app = repository.app_post

        changelog, created = ChangelogPost.objects.get_or_create(
            app=app,
            version=instance.name,
            defaults={
                "published_at": instance.published_at,
                "content": instance.description,
            },
        )
        if created:
            log.info(f"Created {changelog} from Github release event")
    except AppPost.DoesNotExist:
        log.warning(
            f"Repository {repository} is not associated with an AppPost instance."
        )
