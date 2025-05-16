import logging
import re
from typing import Callable

from django.conf import settings
from django.db.models import Q
from github import github_api
from github.events import GithubEvent
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
from github.tasks.api_models import (
    CreateEventPayload,
    Event,
    IssuesEvent,
    PullRequestEvent,
    PushEvent,
    ReleaseEvent,
    Repo,
    User,
    WikiEvent,
    _EventPayload,
)
from requests.structures import CaseInsensitiveDict

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


class UnwantedEvent(Exception):
    """Raised when parsing an event and we decide we want to discard it."""

    pass


class UnknownUser(Exception):

    pass


class UnknownRepository(Exception):
    """Tried to retrieve a repository that is not in our cache."""

    pass


def update_github_user_events():
    url = f"https://api.github.com/users/{OWNER}/events"

    if _polling_allowed():
        update_cycle = GithubEventUpdateCycle.objects.create()

        def _try_create_event(data: dict) -> GithubUserEvent | None:
            try:
                return _create_event(update_cycle, Event.model_validate(data))

            except UnwantedEvent as e:
                log.debug(f"Skipping event {e}")

            except (UnknownRepository, UnknownUser) as e:
                log.warning(f"Failed to create event: {e}")

            except Exception as e:
                log.warning(f"Failed to handle event {data}: {e}")
                raise e

        response = github_api.for_each(url, _try_create_event)

        if response is None:
            # 304 Not Modified
            update_cycle.delete()
            return

        _remember_polling(url, response.headers)

        _flush_caches()
    else:
        log.warning("Polling is disallowed")


def _polling_allowed() -> bool:
    """Check if the previous polling was sufficiently long ago.

    Polling interval is defined in X-Poll-Interval header."""
    previous_poll: GithubPollingEvent | None = GithubPollingEvent.objects.first()
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
    data: Event,
) -> GithubUserEvent | None:
    if data.actor.login != OWNER:
        return None

    event_type = data.type
    if event_type not in SUPPORTED_EVENTS:
        raise UnwantedEvent(event_type)

    log.info(f"Create event {event_type}: {data.repo.name}")

    owner = _get_user(data.actor)
    repo = _get_repo(data.repo)

    event = GithubUserEvent.objects.create(
        update_cycle=parent,
        github_id=data.id,
        user=owner,
        repository=repo,
        type=event_type,
        created_at=data.created_at,
        is_public=data.is_public,
    )

    try:
        create_payload(event_type, event, data.payload)

    except UnwantedEvent:
        # Back-track to delete the event with an unwanted payload.
        event.delete()


def _get_user(user: User) -> GithubUser:
    try:
        return GithubUser.objects.get(id=user.id)
    except GithubUser.DoesNotExist:
        raise UnknownUser(f"Unknown github user: {user.login} [{user.id}]")


def _get_repo(repo: Repo) -> GithubRepository:
    try:
        return GithubRepository.objects.get(id=repo.id)
    except GithubRepository.DoesNotExist:
        raise UnknownRepository(f"Unknown repository: {repo.name} [{repo.id}")


def create_payload[
    T: _EventPayload
](event_type: str, event: GithubUserEvent, data: dict,):
    """Spec: https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types"""

    func: Callable[[GithubUserEvent, T], None]
    payload: T

    if event_type == GithubEvent.CreateEvent:
        payload = CreateEventPayload.model_validate(data)
        func = _create_create_payload

    elif event_type == GithubEvent.WikiEvent:
        payload = WikiEvent.model_validate(data)
        func = _create_wiki_payload

    elif event_type == GithubEvent.IssuesEvent:
        payload = IssuesEvent.model_validate(data)
        func = _create_issues_payload

    elif event_type == GithubEvent.PullRequestEvent:
        payload = PullRequestEvent.model_validate(data)
        func = _create_pullrequest_payload

    elif event_type == GithubEvent.PushEvent:
        payload = PushEvent.model_validate(data)
        func = _create_push_payload

    elif event_type == GithubEvent.ReleaseEvent:
        payload = ReleaseEvent.model_validate(data)
        func = _create_release_event

    else:
        raise UnwantedEvent(event_type)

    func(event, payload)


def _create_create_payload(event: GithubUserEvent, payload: CreateEventPayload):
    GithubCreatePayload.objects.create(
        event=event,
        ref=payload.ref,
        ref_type=payload.ref_type,
        created_at=event.created_at,
    )


def _create_push_payload(event: GithubUserEvent, payload: PushEvent):
    commits = payload.commits

    api_url_regex = re.compile(
        r"^(https://)(api\.)(github\.com/)(repos/)(.*?)$",
        re.MULTILINE,
    )

    def api_to_html_url(url):
        return re.sub(api_url_regex, r"\g<1>\g<3>\g<5>", url)

    for commit in commits:
        GithubCommit.objects.create(
            sha=commit.sha,
            message=commit.message,
            url=api_to_html_url(commit.url),
            event=event,
        )


def _create_pullrequest_payload(event: GithubUserEvent, payload: PullRequestEvent):
    if payload.action == "closed":
        pull_request = payload.pull_request

        if pull_request.is_merged:
            GithubPullRequestMergedPayload.objects.create(
                event=event,
                url=pull_request.html_url,
                number=pull_request.number,
                merged_at=pull_request.merged_at,
                additions_count=pull_request.additions,
                deletions_count=pull_request.deletions,
                changed_files_count=pull_request.changed_files,
            )
            return

    raise UnwantedEvent("PullRequest must be action=closed and is_merged=True.")


def _create_issues_payload(event: GithubUserEvent, payload: IssuesEvent):
    action = payload.action

    if action == "closed":
        issue = payload.issue
        GithubIssueClosedPayload.objects.create(
            event=event,
            number=issue.number,
            url=issue.html_url,
            closed_at=issue.closed_at,
        )
        return

    raise UnwantedEvent("IssuesEvent must be action=closed")


def _create_wiki_payload(event: GithubUserEvent, payload: WikiEvent):
    pages = payload.pages

    for page in pages:
        GithubWikiPayload.objects.create(
            event=event,
            url=page.html_url,
            action=page.action,
            name=page.page_name,
        )


def _create_release_event(event: GithubUserEvent, payload: ReleaseEvent):
    if payload.action == "published":
        release = payload.release
        GithubReleasePublishedPayload.objects.create(
            event=event,
            url=release.html_url,
            name=release.name,
            description=release.description,
            published_at=release.published_at,
        )
        return

    raise UnwantedEvent("ReleaseEvent must be action=published")


def _flush_caches():
    """Delete all but the newest event data."""
    latest = GithubEventUpdateCycle.objects.all().order_by("-created_at").first()

    GithubEventUpdateCycle.objects.filter(~Q(id=latest.pk)).delete()
