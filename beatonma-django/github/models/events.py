from common.models import ApiModel, BaseModel
from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from github import events as github_events
from github.models.repository import GithubRepository, GithubUser


def _get_event_types():
    return getattr(settings, "GITHUB_EVENTS", github_events.all_events())


class GithubEventUpdateCycle(BaseModel):
    """Parent object for every GithubUserEvent retrieved during an update cycle.

    Deleting an instance will delete (via cascade) all the data associated with
    that cycle.
    """

    def __str__(self):
        return f"{self.created_at}: {self.events.count()} events"


class GithubUserEvent(ApiModel, BaseModel):
    """Each event in the event stream returned by
    https://api.github.com/users/{OWNER}/events will create"""

    github_id = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    is_public = models.BooleanField()

    update_cycle = models.ForeignKey(
        GithubEventUpdateCycle,
        on_delete=models.CASCADE,
        related_name="events",
    )

    repository = models.ForeignKey(
        GithubRepository,
        on_delete=models.CASCADE,
        related_name="+",
    )

    user = models.ForeignKey(
        GithubUser,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def publicly_visible(self) -> bool:
        return self.is_public and self.repository.is_published

    def payload(self):
        if self.type == github_events.CREATE_EVENT:
            return self.create_event_data

        elif self.type == github_events.PUSH_EVENT:
            return self.commits.all()

        elif self.type == github_events.ISSUES_EVENT:
            return self.issue_closed_data

        elif self.type == github_events.RELEASE_EVENT:
            return self.release_data

        elif self.type == github_events.WIKI_EVENT:
            return self.wiki_changes.all()

        elif self.type == github_events.PULL_REQUEST_EVENT:
            return self.pull_merged_data

        else:
            raise Exception(
                f"GithubUserEvent.payload: Unsupported event type: {self.type}"
            )

    def payload_changes(self):
        payload = self.payload()
        if isinstance(payload, QuerySet):
            return payload.count()
        return 0

    def to_json(self) -> dict:
        if not self.repository.is_published or not self.is_public:
            return {
                "created_at": self.created_at.isoformat(),
                "type": self.type,
            }

        payload = self.payload()

        if payload is None:
            payload_json = None

        elif isinstance(payload, QuerySet):
            payload_json = [x.to_json() for x in payload.all()]

        else:
            payload_json = payload.to_json()

        return {
            "created_at": self.created_at.isoformat(),
            "id": self.github_id,
            "type": self.type,
            "repository": self.repository.to_json(),
            "payload": payload_json,
        }

    def __str__(self):
        return f"{self.type}: {self.repository}"


class GithubEventPayload(ApiModel, BaseModel):
    class Meta:
        abstract = True


class GithubCommit(GithubEventPayload):
    sha = models.CharField(
        max_length=256,
        editable=False,
    )
    message = models.TextField(editable=False)
    url = models.URLField(editable=False)

    event = models.ForeignKey(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="commits",
    )

    def to_json(self) -> dict:
        return {
            "sha": self.sha,
            "message": self.message,
            "url": self.url,
        }

    def __str__(self):
        return f"{self.sha[:6]}: {self.message[:128]}"

    class Meta:
        verbose_name_plural = "GithubEvents: Commit"


class GithubCreatePayload(GithubEventPayload):
    ref = models.CharField(max_length=128, null=True, editable=False)
    ref_type = models.CharField(max_length=128, editable=False)

    event = models.OneToOneField(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="create_event_data",
    )

    def to_json(self) -> dict:
        return {
            "type": self.ref_type,
            "ref": self.ref,
        }

    def __str__(self):
        return f"Create {self.ref_type}: {self.ref}"

    class Meta:
        verbose_name_plural = "GithubEvents: Create"


class GithubIssuesPayload(GithubEventPayload):
    number = models.PositiveSmallIntegerField(editable=False)
    url = models.URLField(editable=False)
    closed_at = models.DateTimeField(editable=False)

    event = models.OneToOneField(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="issue_closed_data",
    )

    def to_json(self) -> dict:
        return {
            "number": self.number,
            "url": self.url,
            "closed_at": self.closed_at.isoformat(),
        }

    def __str__(self):
        return f"Closed #{self.number}: {self.closed_at}"

    class Meta:
        verbose_name_plural = "GithubEvents: Issue"


class GithubPullRequestPayload(GithubEventPayload):
    url = models.URLField(editable=False)
    number = models.PositiveSmallIntegerField(editable=False)
    merged_at = models.DateTimeField(editable=False)
    additions_count = models.PositiveIntegerField(editable=False)
    deletions_count = models.PositiveIntegerField(editable=False)
    changed_files_count = models.PositiveIntegerField(editable=False)

    event = models.OneToOneField(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="pull_merged_data",
    )

    def to_json(self) -> dict:
        return {
            "number": self.number,
            "url": self.url,
            "merged_at": str(self.merged_at),
            "addition_count": self.additions_count,
            "deletions_count": self.deletions_count,
            "changed_files_count": self.changed_files_count,
        }

    def __str__(self):
        return f"Merged #{self.number}: {self.merged_at}"

    class Meta:
        verbose_name_plural = "GithubEvents: Close pull request"


class GithubReleasePayload(GithubEventPayload):
    name = models.CharField(max_length=256, editable=False)
    url = models.URLField(editable=False)
    description = models.TextField(editable=False)
    published_at = models.DateTimeField(editable=False)

    event = models.OneToOneField(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="release_data",
    )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "published_at": str(self.published_at),
        }

    def __str__(self):
        return f"Release {self.name}: {self.published_at}"

    class Meta:
        verbose_name_plural = "GithubEvents: Release"


class GithubWikiPayload(GithubEventPayload):
    name = models.CharField(max_length=256, editable=False)
    url = models.URLField(editable=False)
    action = models.CharField(max_length=64, editable=False)

    event = models.ForeignKey(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="wiki_changes",
    )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "action": self.action,
        }

    def __str__(self):
        return f"{self.action} {self.name}"

    class Meta:
        verbose_name_plural = "GithubEvents: Wiki edit"
