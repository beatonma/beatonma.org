import logging
from datetime import datetime
from typing import Callable

from django.conf import settings
from requests.structures import CaseInsensitiveDict

from common.util import http
from github import github_api
from github.events import GithubEvent
from github.github_api import GithubBreakForEach
from github.models.api import GithubPollingEvent
from github.models.events import (
    GithubCommit,
    GithubCreatePayload,
    GithubEventUpdateCycle,
    GithubIssueClosedPayload,
    GithubPullRequestMergedPayload,
    GithubReleasePublishedPayload,
    GithubUserEvent,
    GithubWikiPayload,
)
from github.models.repository import GithubRepository, GithubUser
from github.tasks import api_models

log = logging.getLogger(__name__)

OWNER = settings.GITHUB_USERNAME


SUPPORTED_EVENTS = [
    GithubEvent.CreateEvent,
    GithubEvent.WikiEvent,
    GithubEvent.IssuesEvent,
    GithubEvent.PullRequestEvent,
    GithubEvent.PushEvent,
    GithubEvent.ReleaseEvent,
]


def update_github_user_events(
    *, username: str = OWNER, update_cycle: GithubEventUpdateCycle = None
):
    if not update_cycle:
        update_cycle = GithubEventUpdateCycle.objects.create()

    url = github_api.url_user_events(username)

    _update_events(url, update_cycle)


def update_repository_events(
    *, update_cycle: GithubEventUpdateCycle = None, changed_since: datetime = None
):
    if not update_cycle:
        update_cycle = GithubEventUpdateCycle.objects.create()
    repos = GithubRepository.objects.all()
    if changed_since:
        repos = repos.filter(updated_at__gt=changed_since)

    for repo in repos:
        url = github_api.url_repository_events(repo.full_name)
        _update_events(url, update_cycle)


class UnwantedEvent(Exception):
    """Raised when parsing an event and we decide we want to discard it."""

    pass


class UnknownUser(Exception):

    pass


class UnknownRepository(Exception):
    """Tried to retrieve a repository that is not in our cache."""

    pass


def _update_events(url: str, update_cycle: GithubEventUpdateCycle) -> None:
    if not _polling_allowed(url):
        return

    response = github_api.for_each(
        url,
        lambda data: _try_create_event(data, update_cycle),
    )

    if response.status_code == http.STATUS_304_NOT_MODIFIED:
        return

    _remember_polling(url, response.headers)


def _try_create_event(
    data: dict,
    update_cycle: GithubEventUpdateCycle,
) -> GithubUserEvent | None:
    try:
        return _create_event(update_cycle, api_models.Event.model_validate(data))

    except UnwantedEvent as e:
        log.debug(f"Skipping event {e}")

    except (UnknownRepository, UnknownUser) as e:
        log.warning(f"Failed to create event: {e}")

    except Exception as e:
        log.warning(f"Failed to handle event {data}: {e}")
        raise e


def _polling_allowed(url: str) -> bool:
    """Check if the previous polling was sufficiently long ago.

    Polling interval is defined in X-Poll-Interval header."""
    previous_poll: GithubPollingEvent | None = GithubPollingEvent.objects.filter(
        url=url
    ).first()
    if previous_poll and not previous_poll.elapsed():
        log.warning(
            f"Github polling event denied until at least {previous_poll.elapses_at}"
        )
        return False
    return True


def _remember_polling(url: str, headers: CaseInsensitiveDict):
    """Keep a record of the latest polling event so we can respect X-Polling-Interval header."""
    GithubPollingEvent.objects.all().delete()
    polling_interval = headers.get("X-Poll-Interval")

    GithubPollingEvent.objects.create(url=url, interval=int(polling_interval))


def _create_event(
    parent: GithubEventUpdateCycle,
    data: api_models.Event,
) -> GithubUserEvent | None:
    if data.actor.login != OWNER:
        return None

    event_type = data.type
    if event_type not in SUPPORTED_EVENTS:
        raise UnwantedEvent(event_type)

    log.info(f"Create event {event_type}: {data.repo.name}")

    owner = _get_user(data.actor)
    repo = _get_repo(data.repo)

    event, created = GithubUserEvent.objects.get_or_create(
        github_id=data.id,
        defaults={
            "update_cycle": parent,
            "user": owner,
            "repository": repo,
            "type": event_type,
            "created_at": data.created_at,
            "is_public": data.is_public,
        },
    )

    if created:
        try:
            create_payload(event_type, event, data.payload)

        except UnwantedEvent:
            # Back-track to delete the event with an unwanted payload.
            event.delete()
    return event


def _get_user(user: api_models.User) -> GithubUser:
    try:
        return GithubUser.objects.get(id=user.id)
    except GithubUser.DoesNotExist:
        raise UnknownUser(f"Unknown github user: {user.login} [{user.id}]")


def _get_repo(repo: api_models.Repo) -> GithubRepository:
    try:
        return GithubRepository.objects.get(id=repo.id)
    except GithubRepository.DoesNotExist:
        raise UnknownRepository(f"Unknown repository: {repo.name} [{repo.id}")


def create_payload[T: api_models.EventPayload](
    event_type: str,
    event: GithubUserEvent,
    data: dict,
):
    """Spec: https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types"""

    func: Callable[[GithubUserEvent, T], None]
    payload: T

    if event_type == GithubEvent.CreateEvent:
        payload = api_models.CreateEventPayload.model_validate(data)
        func = _create_create_payload

    elif event_type == GithubEvent.WikiEvent:
        payload = api_models.WikiEvent.model_validate(data)
        func = _create_wiki_payload

    elif event_type == GithubEvent.IssuesEvent:
        payload = api_models.IssuesEvent.model_validate(data)
        func = _create_issues_payload

    elif event_type == GithubEvent.PullRequestEvent:
        payload = api_models.PullRequestEvent.model_validate(data)
        func = _create_pullrequest_payload

    elif event_type == GithubEvent.PushEvent:
        payload = api_models.PushEvent.model_validate(data)
        func = _create_push_payload

    elif event_type == GithubEvent.ReleaseEvent:
        payload = api_models.ReleaseEvent.model_validate(data)
        func = _create_release_event

    else:
        raise UnwantedEvent(event_type)

    func(event, payload)


def _create_create_payload(
    event: GithubUserEvent, payload: api_models.CreateEventPayload
):
    GithubCreatePayload.objects.get_or_create(
        event=event,
        ref=payload.ref,
        ref_type=payload.ref_type,
        defaults={
            "created_at": event.created_at,
        },
    )


def _create_push_payload(event: GithubUserEvent, payload: api_models.PushEvent):
    current_ref = payload.head
    previous_ref = payload.before

    def _create_commit(raw_commit_data: dict) -> None:
        commit_data: api_models.Commit = api_models.Commit.model_validate(
            raw_commit_data
        )
        sha = commit_data.sha

        if sha == previous_ref:
            raise GithubBreakForEach(f"Previous commit SHA reached: {sha}")

        commit, created = GithubCommit.objects.update_or_create(
            event=event,
            sha=sha,
            defaults={
                "created_at": commit_data.timestamp,
                "message": commit_data.message,
                "url": commit_data.html_url,
            },
        )

        if not created:
            raise GithubBreakForEach(f"GithubCommit already retrieved: {sha}")

    github_api.for_each(
        github_api.url_repository_commits(event.repository.full_name, current_ref),
        _create_commit,
    )


def _create_pullrequest_payload(
    event: GithubUserEvent, payload: api_models.PullRequestEvent
):
    if payload.action == "closed":
        response = github_api.get_if_changed(
            github_api.url_repository_pullrequest(
                event.repository.full_name, payload.number
            )
        )

        pull_request = api_models.PullRequest.model_validate(response.json())
        if pull_request.is_merged:
            GithubPullRequestMergedPayload.objects.get_or_create(
                event=event,
                number=pull_request.number,
                defaults={
                    "url": pull_request.html_url,
                    "merged_at": pull_request.merged_at,
                    "additions_count": pull_request.additions,
                    "deletions_count": pull_request.deletions,
                    "changed_files_count": pull_request.changed_files,
                },
            )
            return

    raise UnwantedEvent("PullRequest must be action=closed and is_merged=True.")


def _create_issues_payload(event: GithubUserEvent, payload: api_models.IssuesEvent):
    action = payload.action

    if action == "closed":
        issue = payload.issue
        GithubIssueClosedPayload.objects.get_or_create(
            event=event,
            number=issue.number,
            defaults={
                "url": issue.html_url,
                "closed_at": issue.closed_at,
            },
        )
        return

    raise UnwantedEvent("IssuesEvent must be action=closed")


def _create_wiki_payload(event: GithubUserEvent, payload: api_models.WikiEvent):
    pages = payload.pages

    for page in pages:
        GithubWikiPayload.objects.get_or_create(
            event=event,
            url=page.html_url,
            action=page.action,
            name=page.page_name,
        )


def _create_release_event(event: GithubUserEvent, payload: api_models.ReleaseEvent):
    if payload.action == "published":
        release = payload.release
        GithubReleasePublishedPayload.objects.get_or_create(
            event=event,
            name=release.name,
            defaults={
                "url": release.html_url,
                "description": release.description,
                "published_at": release.published_at,
            },
        )
        return

    raise UnwantedEvent("ReleaseEvent must be action=published")
