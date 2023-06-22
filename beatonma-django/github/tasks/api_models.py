import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional

from github.tasks.util import parse_datetime


@dataclass
class User:
    id: int
    login: str
    display_login: str
    gravatar_id: str
    url: str
    avatar_url: str


@dataclass
class Repo:
    id: int
    name: str
    url: str


class Event:
    id: int
    type: str
    actor: User
    repo: Repo
    payload: dict
    is_public: bool
    created_at: Optional[datetime.datetime]

    def __init__(
        self,
        id: str,
        type: str,
        actor: dict,
        repo: dict,
        payload: dict,
        public: bool,
        created_at: str,
    ):
        self.id = int(id)
        self.type = type
        self.actor = User(**actor)
        self.repo = Repo(**repo)
        self.payload = payload
        self.is_public = public
        self.created_at = parse_datetime(created_at)


class _EventPayload:
    pass


@dataclass
class CreateEventPayload(_EventPayload):
    ref: Optional[str]
    ref_type: str
    master_branch: str
    description: str
    pusher_type: str


class WikiPage:
    page_name: str
    title: str
    action: str
    sha: str
    html_url: str

    def __init__(
        self,
        page_name: str,
        title: str,
        action: str,
        sha: str,
        html_url: str,
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.title = title
        self.sha = sha
        self.action = action
        self.html_url = html_url
        self.page_name = page_name


class WikiEvent(_EventPayload):
    pages: List[WikiPage]

    def __init__(self, pages: List[Dict]):
        self.pages = [WikiPage(**page) for page in pages]


class Issue:
    html_url: str
    number: int
    closed_at: Optional[datetime.datetime]

    def __init__(
        self,
        html_url: str,
        number: int,
        closed_at: str,
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.html_url = html_url
        self.number = number
        self.closed_at = parse_datetime(closed_at)


class IssuesEvent(_EventPayload):
    action: str
    issue: Issue

    def __init__(self, action: str, issue: Dict):
        self.action = action
        self.issue = Issue(**issue)


class PullRequest:
    url: str
    number: int
    is_merged: bool
    merged_at: Optional[datetime.datetime]
    additions: int
    deletions: int
    changed_files: int

    def __init__(
        self,
        html_url: str,
        number: int,
        merged: bool,
        merged_at: str,
        additions: int,
        deletions: int,
        changed_files: int,
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.url = html_url
        self.number = number
        self.is_merged = merged
        self.merged_at = parse_datetime(merged_at)
        self.additions = additions
        self.deletions = deletions
        self.changed_files = changed_files


class PullRequestEvent(_EventPayload):
    action: str
    pull_request: PullRequest

    def __init__(
        self,
        action: str,
        pull_request: dict,
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.action = action
        self.pull_request = PullRequest(**pull_request)


@dataclass
class Commit:
    sha: str
    author: dict
    message: str
    distinct: bool
    url: str


class PushEvent(_EventPayload):
    commits: List[Commit]

    def __init__(
        self,
        commits: List[Dict],
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.commits = [Commit(**c) for c in commits]


class Release:
    html_url: str
    name: str
    description: str
    published_at: Optional[datetime.datetime]

    def __init__(
        self,
        html_url: str,
        name: str,
        body: str,
        published_at: str,
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.html_url = html_url
        self.name = name
        self.description = body
        self.published_at = parse_datetime(published_at)


class ReleaseEvent(_EventPayload):
    action: str
    release: Release

    def __init__(
        self,
        action: str,
        release: dict,
        **kwargs,  # noqa: Other arguments ignored.
    ):
        self.action = action
        self.release = Release(**release)
