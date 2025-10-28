from datetime import datetime
from typing import Literal

from ninja import Schema
from pydantic import Field

from github.tasks.util import parse_datetime

type SHA = str


class User(Schema):
    id: int
    login: str
    display_login: str
    gravatar_id: str
    url: str
    avatar_url: str


class Repo(Schema):
    id: int
    name: str
    url: str


class Event(Schema):
    id: int
    type: str
    actor: User
    repo: Repo
    payload: dict
    is_public: bool = Field(validation_alias="public")
    created_at: datetime | None


class EventPayload(Schema):
    pass


class CreateEventPayload(EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#createevent"""

    ref: SHA | None
    ref_type: Literal["branch", "tag", "repository"]
    master_branch: str
    description: str | None
    pusher_type: str


class WikiPage(Schema):
    page_name: str
    title: str
    action: Literal["created", "edited"]
    sha: SHA
    html_url: str


class WikiEvent(EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#gollumevent"""

    pages: list[WikiPage]


class Issue(Schema):
    html_url: str
    number: int
    closed_at: datetime | None


class IssuesEvent(EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#issuesevent"""

    action: str
    issue: Issue


class PullRequest(Schema):
    html_url: str
    number: int
    is_merged: bool = Field(validation_alias="merged")
    merged_at: datetime | None
    additions: int
    deletions: int
    changed_files: int


class PullRequestEvent(EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#pullrequestevent"""

    action: Literal[
        "opened", "closed", "reopened", "assigned", "unassigned", "labeled", "unlabeled"
    ]
    number: int


class Commit(Schema):
    """https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28&versionId=free-pro-team%40latest&category=git&subcategory=commits"""

    sha: SHA
    message: str
    api_url: str = Field(validation_alias="url")
    html_url: str
    timestamp: datetime

    @staticmethod
    def resolve_message(obj) -> str:
        return obj["commit"]["message"]

    @staticmethod
    def resolve_timestamp(obj) -> datetime:
        return parse_datetime(obj["commit"]["committer"]["date"])


class PushEvent(EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#event-payload-object-for-pushevent"""

    head: SHA
    before: SHA


class Release(Schema):
    html_url: str
    name: str
    description: str = Field(validation_alias="body")
    published_at: datetime | None


class ReleaseEvent(EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#releaseevent"""

    action: Literal["published"]
    release: Release
