from datetime import datetime
from typing import List, Optional, Set

from celery import shared_task
from common.models import ApiModel
from django.conf import settings
from django.db.models import QuerySet
from django.utils.timezone import get_current_timezone
from github.models import CachedResponse, GithubEventUpdateCycle, GithubUserEvent

from ..events import GithubEvent
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
        CachedResponse.objects.create(data=_aggregate_events_json(update.events.all()))


class _PrivateEventsSummary(ApiModel):
    event_count: int
    change_count: int
    _repository_ids: Set[int]
    latest_timestamp: datetime

    def __init__(self):
        self.event_count = 0
        self.change_count = 0
        self._repository_ids = set()
        self.latest_timestamp = datetime(1, 1, 1, tzinfo=get_current_timezone())

    def add(self, event: GithubUserEvent):
        self.event_count += 1
        self.change_count += event.payload_changes()
        self._repository_ids.add(event.repository.pk)
        self.latest_timestamp = sorted([self.latest_timestamp, event.created_at])[1]

    def to_json(self) -> dict:
        return {
            "type": "PrivateEventSummary",
            "created_at": self.latest_timestamp.isoformat(),
            "repository_count": len(self._repository_ids),
            "event_count": self.event_count,
            "change_count": self.change_count,
        }


def _get_event_types():
    return getattr(settings, "GITHUB_EVENTS", GithubEvent.values())


def _aggregate_events_json(events: QuerySet[GithubUserEvent]) -> List[dict]:
    """Combine consecutive private events into a single summary object."""

    private_event_aggregator: Optional[_PrivateEventsSummary] = None
    results = []

    def _store_aggregator():
        nonlocal private_event_aggregator
        if private_event_aggregator is not None:
            results.append(private_event_aggregator.to_json())
            private_event_aggregator = None

    for event in events:
        if event.publicly_visible():
            _store_aggregator()
            results.append(event.to_json())
            continue

        if private_event_aggregator is None:
            private_event_aggregator = _PrivateEventsSummary()

        private_event_aggregator.add(event)

    if private_event_aggregator is not None:
        results.append(private_event_aggregator.to_json())

    return results
