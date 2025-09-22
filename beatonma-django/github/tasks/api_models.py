from datetime import datetime
from typing import Literal

from ninja import Schema
from pydantic import Field


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


class _EventPayload(Schema):
    pass


class CreateEventPayload(_EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#createevent"""

    ref: str | None
    ref_type: Literal["branch", "tag", "repository"]
    master_branch: str
    description: str | None
    pusher_type: str


class WikiPage(Schema):
    page_name: str
    title: str
    action: Literal["created", "edited"]
    sha: str
    html_url: str


class WikiEvent(_EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#gollumevent"""

    pages: list[WikiPage]


class Issue(Schema):
    html_url: str
    number: int
    closed_at: datetime | None


class IssuesEvent(_EventPayload):
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


class PullRequestEvent(_EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#pullrequestevent"""

    action: str
    pull_request: PullRequest


class Commit(Schema):
    sha: str
    author: dict
    message: str
    distinct: bool
    url: str


class PushEvent(_EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#pushevent"""

    commits: list[Commit]


class Release(Schema):
    html_url: str
    name: str
    description: str = Field(validation_alias="body")
    published_at: datetime | None


class ReleaseEvent(_EventPayload):
    """https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#releaseevent"""

    action: str
    release: Release
