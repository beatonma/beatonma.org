from django.db import models

from common.models import BaseModel, PublishedMixin, SortableMixin
from main.models.mixins.cache import GlobalStateCacheMixin


class Feed(SortableMixin, PublishedMixin, GlobalStateCacheMixin, BaseModel):
    search_fields = []

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name


class FeedsMixin(models.Model):
    class Meta:
        abstract = True

    DEFAULT_FEED_SLUG = "everything"

    default_feeds: list[tuple[str, str]] = [
        (DEFAULT_FEED_SLUG, "Everything"),
    ]

    feeds = models.ManyToManyField(Feed)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._apply_default_feeds()

    def _apply_default_feeds(self):
        for slug, name in self.default_feeds:
            self.add_feed(name, slug)

    def add_feed(self, name: str, slug: str):
        f, _ = Feed.objects.get_or_create(slug=slug, defaults={"name": name})
        self.feeds.add(f)

    @classmethod
    def get_default_feeds(cls) -> list[Feed]:
        feeds = []
        for slug, name in cls.default_feeds:
            f, _ = Feed.objects.get_or_create(slug=slug, defaults={"name": name})
            feeds.append(f)
        return feeds
