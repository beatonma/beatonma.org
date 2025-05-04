from common.models import BaseModel
from django.db import models
from django.db.models import QuerySet
from github.events import GithubEvent
from github.models.repository import GithubRepository, GithubUser


class GithubEventUpdateCycle(BaseModel):
    """Parent object for every GithubUserEvent retrieved during an update cycle.

    Deleting an instance will delete (via cascade) all the data associated with
    that cycle.
    """

    def __str__(self):
        return f"{self.created_at}: {self.events.count()} events"


class GithubUserEvent(BaseModel):
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
        if self.type == GithubEvent.CreateEvent:
            return self.create_event_data

        elif self.type == GithubEvent.PushEvent:
            return self.commits.all()

        elif self.type == GithubEvent.IssuesEvent:
            return self.issue_closed_data

        elif self.type == GithubEvent.ReleaseEvent:
            return self.release_data

        elif self.type == GithubEvent.WikiEvent:
            return self.wiki_changes.all()

        elif self.type == GithubEvent.PullRequestEvent:
            return self.pull_merged_data

        else:
            raise Exception(
                f"GithubUserEvent.payload: Unsupported event type: {self.type}"
            )

    def payload_changes(self):
        payload = self.payload()
        if isinstance(payload, QuerySet):
            return payload.count()
        return 1

    def __str__(self):
        return f"{self.type}: {self.repository}"


class GithubEventPayload(BaseModel):
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

    def __str__(self):
        return f"Create {self.ref_type}: {self.ref}"

    class Meta:
        verbose_name_plural = "GithubEvents: Create"


class GithubIssueClosedPayload(GithubEventPayload):
    number = models.PositiveSmallIntegerField(editable=False)
    url = models.URLField(editable=False)
    closed_at = models.DateTimeField(editable=False)

    event = models.OneToOneField(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="issue_closed_data",
    )

    def __str__(self):
        return f"Closed #{self.number}: {self.closed_at}"

    class Meta:
        verbose_name_plural = "GithubEvents: Issue"


class GithubPullRequestMergedPayload(GithubEventPayload):
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

    def __str__(self):
        return f"Merged #{self.number}: {self.merged_at}"

    class Meta:
        verbose_name_plural = "GithubEvents: Close pull request"


class GithubReleasePublishedPayload(GithubEventPayload):
    name = models.CharField(max_length=256, editable=False)
    url = models.URLField(editable=False)
    description = models.TextField(editable=False)
    published_at = models.DateTimeField(editable=False)

    event = models.OneToOneField(
        GithubUserEvent,
        on_delete=models.CASCADE,
        related_name="release_data",
    )

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

    def __str__(self):
        return f"{self.action} {self.name}"

    class Meta:
        verbose_name_plural = "GithubEvents: Wiki edit"
