from celery import shared_task
from contact.tasks import send_notification
from github import api
from github.models import CachedResponse, GithubEventUpdateCycle

from .update_events import update_github_user_events
from .update_repositories import update_github_repository_cache


@shared_task
def update_github_repos_and_events():
    try:
        update_github_repository_cache()
        update_github_user_events()

        prebuild_cached_response()
    except Exception as e:
        send_notification(
            "Github update error", str(e), color="#C70036", important=True
        )
        raise e


def prebuild_cached_response():
    """Precompute the JSON data for GithubEventsView."""
    update: GithubEventUpdateCycle = GithubEventUpdateCycle.objects.first()

    if update:
        CachedResponse.objects.all().delete()
        CachedResponse.objects.create(
            data=api.build_response(update.events.all()).model_dump()
        )
