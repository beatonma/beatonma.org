from common.models import BaseModel, PublishedMixin
from django.db import models
from main.models.mixins.cache import GlobalStateCacheMixin


class Feed(PublishedMixin, GlobalStateCacheMixin, BaseModel):
    search_fields = []

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64)

    def __str__(self):
        return self.name


class FeedsMixin(models.Model):
    class Meta:
        abstract = True

    default_feeds: list[tuple[str, str]]

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
