from common.models.search import SearchMixin, SearchQuerySet
from django.db import models
from django.utils import timezone

_null_datetime = timezone.make_aware(timezone.datetime.min)


class PublishedQuerySet(SearchQuerySet):
    """Overrides default methods to keep unpublished objects hidden."""

    def filter(self, *args, dangerous_all: bool = False, **kwargs):
        if dangerous_all:
            return super().filter(*args, **kwargs)

        return super().filter(*args, **kwargs, is_published=True)

    def all(self):
        return self.published()

    def published(self):
        return super().filter(is_published=True)

    def get_private__dangerous__(self):
        return super().filter(is_published=False)


class PublishedMixin(SearchMixin, models.Model):
    class Meta:
        abstract = True
        ordering = "-published_at"

    objects = PublishedQuerySet.as_manager()

    is_published = models.BooleanField(default=True, help_text="Publicly visible")
    published_at = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        self._enforce_objects_manager_type()

        super().__init__(*args, **kwargs)

    def _enforce_objects_manager_type(self):
        """Ensure that `Model.objects` correctly inherits PublishedQuerySet.

        Neglecting to do so could allow non-published content to be accessible."""

        objects_class = self.__class__.objects._queryset_class
        assert issubclass(
            objects_class, PublishedQuerySet
        ), f"Model `{self.__class__.__name__}` inherits `PublishedMixin` but manager does not inherit `PublishedQuerySet`! (Found {objects_class.__name__})"

    def get_sorting_datetime(self) -> timezone.datetime:
        """Return a datetime to be used for sorting."""
        return self.published_at
