from datetime import datetime
from typing import Literal

from django.db.models import QuerySet
from django.http import Http404, HttpRequest
from django.utils.timezone import get_current_timezone
from github.events import GithubEvent
from github.models import CachedResponse, GithubUserEvent
from ninja import Router, Schema

router = Router(tags=["Github"])


def _resolve_value(obj, key):
    """Get the value of obj.key or obj[key]."""
    try:
        return getattr(obj, key)
    except AttributeError:
        return obj.get(key)


class PayloadSchema(Schema):
    pass


class GithubRepositorySchema(PayloadSchema):
    id: int
    name: str
    url: str
    license: str | None
    description: str | None

    @staticmethod
    def resolve_license(obj) -> str | None:
        _license = _resolve_value(obj, "license")
        if _license is None:
            return None
        if isinstance(_license, str):
            return _license
        return _resolve_value(_license, "name")


class GithubCreateEventPayload(PayloadSchema):
    ref_type: Literal["branch", "tag", "repository"]
    ref: str


class GithubIssueEventPayload(PayloadSchema):
    number: int
    url: str
    closed_at: datetime


class GithubPullRequestPayload(PayloadSchema):
    number: int
    url: str
    merged_at: datetime
    additions_count: int
    deletions_count: int
    changed_files_count: int


class GithubCommit(PayloadSchema):
    sha: str
    message: str
    url: str


class GithubWikiEdit(PayloadSchema):
    name: str
    url: str
    action: Literal["created", "edited"]


class GithubReleasePayload(PayloadSchema):
    name: str
    url: str
    description: str
    published_at: datetime


class BaseEventSchema(Schema):
    type: GithubEvent | Literal["PrivateEventSummary"]
    created_at: datetime


class PublicEventSchema[Payload: PayloadSchema | list[PayloadSchema]](BaseEventSchema):
    type: GithubEvent
    id: int
    repository: GithubRepositorySchema
    payload: Payload


class GithubPublicCreateEvent(PublicEventSchema[GithubCreateEventPayload]):
    type: Literal[GithubEvent.CreateEvent]


class GithubPublicIssueEvent(PublicEventSchema[GithubIssueEventPayload]):
    type: Literal[GithubEvent.IssuesEvent]


class GithubPublicPullRequestEvent(PublicEventSchema[GithubPullRequestPayload]):
    type: Literal[GithubEvent.PullRequestEvent]


class GithubPublicReleaseEvent(PublicEventSchema[GithubReleasePayload]):
    type: Literal[GithubEvent.ReleaseEvent]


class GithubPublicPushEvent(PublicEventSchema[list[GithubCommit]]):
    type: Literal[GithubEvent.PushEvent]


class GithubPublicWikiEvent(PublicEventSchema[list[GithubWikiEdit]]):
    type: Literal[GithubEvent.WikiEvent]


class GithubPrivateEvent(BaseEventSchema):
    type: Literal["PrivateEventSummary"]
    event_count: int
    change_count: int
    repository_count: int


class GithubRecentEvents(Schema):
    events: list[
        GithubPrivateEvent
        | GithubPublicCreateEvent
        | GithubPublicIssueEvent
        | GithubPublicPullRequestEvent
        | GithubPublicReleaseEvent
        | GithubPublicPushEvent
        | GithubPublicWikiEvent
    ]


@router.get("/recent/", response=GithubRecentEvents)
def get_github_events(request: HttpRequest):
    cached_response = CachedResponse.objects.first()
    if not cached_response:
        raise Http404()

    return cached_response.data


def build_response(events: QuerySet[GithubUserEvent]) -> GithubRecentEvents:
    """Combine consecutive private events into a single summary object."""

    aggregator: _PrivateEventsSummary | None = None
    results: list[dict] = []

    def store_private_summary():
        nonlocal aggregator
        if aggregator:
            results.append(aggregator.to_schema())
            aggregator = None

    for event in events:
        if event.publicly_visible():
            store_private_summary()
            results.append(_public_event_to_schema(event))
            continue

        if not aggregator:
            aggregator = _PrivateEventsSummary()

        aggregator.add(event)

    store_private_summary()

    return GithubRecentEvents.model_validate({"events": results})


class _PrivateEventsSummary:
    event_count: int
    change_count: int
    _repository_ids: set[int]
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

    def to_schema(self):
        return GithubPrivateEvent.model_validate(
            {
                "type": "PrivateEventSummary",
                "created_at": self.latest_timestamp,
                "repository_count": len(self._repository_ids),
                "event_count": self.event_count,
                "change_count": self.change_count,
            }
        )


def _public_event_to_schema(event: GithubUserEvent):
    return {
        GithubEvent.CreateEvent: GithubPublicCreateEvent,
        GithubEvent.IssuesEvent: GithubPublicIssueEvent,
        GithubEvent.PullRequestEvent: GithubPublicPullRequestEvent,
        GithubEvent.ReleaseEvent: GithubPublicReleaseEvent,
        GithubEvent.PushEvent: GithubPublicPushEvent,
        GithubEvent.WikiEvent: GithubPublicWikiEvent,
    }[event.type].from_orm(event)
