from django.db import models
from django.utils import timezone

from common.models import BaseModel


class GithubPollingEvent(BaseModel):
    """Used to track polling to obey X-Poll-Interval header.

    https://docs.github.com/en/rest/reference/activity#events"""

    url = models.URLField()

    # Minimum number of seconds from this event to the next.
    interval = models.PositiveSmallIntegerField()

    @property
    def elapses_at(self) -> timezone.datetime:
        return self.created_at + timezone.timedelta(seconds=self.interval)

    def elapsed(self, now: timezone.datetime = None) -> bool:
        """Return True if the required interval since this event has passed."""
        if now is None:
            now = timezone.now()

        return now > self.elapses_at

    def __str__(self):
        return f"{self.url}: {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "GithubEvents: Polling event"


class GithubETag(BaseModel):
    """A tag included in each response. Used to check for changes.

    See: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#conditional-requests
    """

    url = models.URLField(unique=True, primary_key=True, editable=False)
    etag = models.CharField(
        max_length=256,
        unique=True,
        editable=False,
    )
    timestamp = models.DateTimeField(editable=False)

    def __str__(self):
        return f"{self.url}: {self.timestamp}"

    class Meta:
        ordering = ["url"]
