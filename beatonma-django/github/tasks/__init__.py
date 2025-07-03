from datetime import datetime

from celery import shared_task
from contact.tasks import send_notification
from github import api
from github.models import CachedResponse, GithubEventUpdateCycle, GithubUserEvent

from .update_events import update_github_user_events, update_repository_events
from .update_repositories import update_github_repository_cache


@shared_task
def update_github_repos_and_events():
    previous_update: datetime | None = None
    if latest := GithubEventUpdateCycle.objects.all().order_by("-created_at").first():
        previous_update = latest.created_at

    try:
        cycle = GithubEventUpdateCycle.objects.create()

        update_github_repository_cache()
        update_github_user_events(update_cycle=cycle)
        update_repository_events(update_cycle=cycle, changed_since=previous_update)

        print(cycle.events.all())

        prebuild_cached_response()
    except Exception as e:
        send_notification(
            "Github update error", str(e), color="#C70036", important=True
        )
        raise e


def prebuild_cached_response():
    """Precompute the JSON data for GithubEventsView."""
    events = GithubUserEvent.objects.all()

    if events.exists():
        CachedResponse.objects.all().delete()
        CachedResponse.objects.create(
            data=api.build_response(events[:100]).model_dump()
        )
