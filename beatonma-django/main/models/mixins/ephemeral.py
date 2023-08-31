import logging
from datetime import datetime
from typing import Optional

from common.models import BaseModel, PublishedMixin
from common.models.published import PublishedQuerySet
from django.db import models
from django.db.models import Q
from django.utils import timezone

log = logging.getLogger(__name__)


class EphemeralQuerySet(PublishedQuerySet):
    def get_for_datetime(self, time: datetime) -> Optional["EphemeralMixin"]:
        return (
            self.published()
            .filter(Q(public_from__isnull=True) | Q(public_from__lte=time))
            .filter(Q(public_until__isnull=True) | Q(public_until__gt=time))
            .order_by("-created_at")
            .first()
        )

    def get_current(self) -> Optional["EphemeralMixin"]:
        return self.get_for_datetime(timezone.now())


class EphemeralMixin(PublishedMixin, BaseModel):
    """Represents something that only exists for some length of time."""

    objects = EphemeralQuerySet.as_manager()

    public_from = models.DateTimeField(null=True, blank=True)
    public_until = models.DateTimeField(null=True, blank=True)

    def is_active(self) -> bool:
        """Return True if constraints allow this item to be viewable at the current moment."""
        now = timezone.now()
        return (
            self.is_published
            and (self.public_from is None or self.public_from <= now)
            and (self.public_until is None or self.public_until > now)
        )

    class Meta:
        abstract = True
