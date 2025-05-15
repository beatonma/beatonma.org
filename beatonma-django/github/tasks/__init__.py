from celery import shared_task
from github import api
from github.models import CachedResponse, GithubEventUpdateCycle

from .update_events import update_github_user_events
from .update_repositories import update_github_repository_cache


@shared_task
def update_github_repos_and_events():
    update_github_repository_cache()
    update_github_user_events()

    prebuild_cached_response()


def prebuild_cached_response():
    """Precompute the JSON data for GithubEventsView."""
    update: GithubEventUpdateCycle = GithubEventUpdateCycle.objects.first()

    if update:
        CachedResponse.objects.all().delete()
        CachedResponse.objects.create(
            data=api.build_response(update.events.all()).model_dump()
        )
