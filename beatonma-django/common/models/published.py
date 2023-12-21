import logging
from typing import Iterable, Optional, cast

from common.models.search import SearchMixin, SearchQuerySet
from django.db import models
from django.db.models import F, QuerySet
from django.utils import timezone
from main.view_adapters import FeedItemContext

log = logging.getLogger(__name__)

_null_datetime = timezone.make_aware(timezone.datetime.min)


class PublishedQuerySet(SearchQuerySet):
    """Overrides default methods to keep unpublished objects hidden."""

    def filter(self, *args, **kwargs):
        return cast(PublishedQuerySet, super().filter(*args, **kwargs))

    def build_search_filter(self, *args, **kwargs) -> QuerySet:
        return super().build_search_filter(*args, **kwargs).filter(is_published=True)

    def published(self):
        return self.filter(is_published=True, published_at__lte=timezone.now())

    def get_private__dangerous__(self):
        return self.filter(is_published=False)

    def sort_by_recent(self):
        return self.order_by(F("published_at").desc(nulls_last=True))


class PublishedMixin(SearchMixin, models.Model):
    class Meta:
        abstract = True
        ordering = "-published_at"

    objects = PublishedQuerySet.as_manager()

    """A list of fields which resolve to other PublishedMixin instances."""
    is_publishable_dependencies: Optional[Iterable[str]] = None

    is_published = models.BooleanField(default=True, help_text="Publicly visible")
    published_at = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        self._enforce_objects_manager_type()

        super().__init__(*args, **kwargs)

    def _enforce_objects_manager_type(self):
        """Ensure that `Model.objects` correctly inherits PublishedQuerySet.

        Neglecting to do so could allow non-published content to be accessible."""

        objects_class = self.__class__.objects._queryset_class
        assert issubclass(objects_class, PublishedQuerySet), (
            f"Model `{self.__class__.__name__}` inherits `PublishedMixin` "
            f"but manager does not inherit `PublishedQuerySet`! "
            f"(Found {objects_class.__name__})"
        )

    def is_publishable(self) -> bool:
        """Return False if this or any dependency has is_published=False."""
        if not self.is_published:
            return False

        if self.is_publishable_dependencies is None:
            return True

        for dependency_field in self.is_publishable_dependencies:
            dependency = getattr(self, dependency_field)
            if dependency is not None and not dependency.is_publishable():
                return False

        return True

    def get_sorting_datetime(self) -> timezone.datetime:
        """Return a datetime to be used for sorting."""
        return self.published_at

    def to_feeditem_context(self) -> FeedItemContext:
        raise NotImplemented(
            f"Model `{self.__class__.__name__}` inherits `PublishedMixin` "
            f"but does not implement `feeditem_context(self)`"
        )
