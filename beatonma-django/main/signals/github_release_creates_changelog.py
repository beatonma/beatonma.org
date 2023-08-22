import logging
from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver
from github.models import GithubReleasePayload
from main.models import App, Changelog
from main.models.posts.formats import Formats

log = logging.getLogger(__name__)


@receiver(
    post_save,
    sender=GithubReleasePayload,
    dispatch_uid="create_changelog_from_githubreleasepayload",
)
def create_changelog_from_githubreleasepayload(
    sender: Type,
    instance: GithubReleasePayload,
    **kwargs,
):
    repository = instance.event.repository
    if not repository.is_public():
        return

    try:
        app = repository.app

        _, created = Changelog.objects.get_or_create(
            app=app,
            version_name=instance.name,
            defaults={
                "format": Formats.MARKDOWN,
                "published_at": instance.published_at,
                "content": instance.description,
            },
        )
        if created:
            log.info(
                f"Created Changelog '{app.title} {instance.name}' from Github event"
            )

    except App.DoesNotExist:
        log.warning(f"Repository {repository} is not associated with an App instance.")
        pass
