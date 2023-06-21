from celery import shared_task

from ..models import CachedResponse, GithubEventUpdateCycle
from .update_events import update_github_user_events
from .update_repositories import update_github_repository_cache


@shared_task
def update_github_repos_and_events():
    update_github_repository_cache()
    update_github_user_events()

    updates: GithubEventUpdateCycle = GithubEventUpdateCycle.objects.first()

    if updates:
        # Pre-build a response for GithubEventsView.
        CachedResponse.objects.all().delete()
        CachedResponse.objects.create(data=updates.to_json())
