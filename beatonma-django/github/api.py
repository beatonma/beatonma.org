from datetime import datetime
from typing import List

from django.http import HttpRequest
from github.events import GithubEvent
from github.models import CachedResponse
from ninja import NinjaAPI, Schema

github_api = NinjaAPI(
    docs_url="/",
    title="Github API",
)


class PayloadSchema(Schema):
    pass


class GithubRepositorySchema(PayloadSchema):
    id: int
    name: str
    url: str
    license: str | None
    description: str | None


class CreateEventPayload(PayloadSchema):
    type: str
    ref: str


class IssueEventPayload(PayloadSchema):
    number: int
    url: str
    closed_at: str


class PullRequestPayload(PayloadSchema):
    number: int
    url: str
    merged_at: str
    addition_count: int
    deletion_count: int
    changed_files_count: int


class Commit(PayloadSchema):
    sha: str
    message: str
    url: str


class WikiEdit(PayloadSchema):
    name: str
    url: str
    action: str


class ReleasePayload(PayloadSchema):
    name: str
    url: str
    description: str
    published_at: str


class GithubEventSchema[Payload: PayloadSchema](Schema):
    type: GithubEvent
    created_at: datetime
    id: int
    repository: GithubRepositorySchema
    payload: Payload


class PrivateEventSchema(Schema):
    type: str
    created_at: datetime
    event_count: int
    change_count: int
    repository_count: int


@github_api.get(
    "/events/",
    response=List[
        PrivateEventSchema
        | GithubEventSchema[CreateEventPayload]
        | GithubEventSchema[IssueEventPayload]
        | GithubEventSchema[PullRequestPayload]
        | GithubEventSchema[ReleasePayload]
        | GithubEventSchema[List[Commit]]
        | GithubEventSchema[List[WikiEdit]]
    ],
)
def get_github_events(request: HttpRequest):
    cached_response = CachedResponse.objects.first()

    events = cached_response.data if cached_response else []
    return events
