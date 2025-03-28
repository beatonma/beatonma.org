import logging
from itertools import chain
from typing import Type

from main.models import AppPost, ChangelogPost, Post
from main.models.rewrite.post import BasePost

log = logging.getLogger(__name__)


type FeedItem = BasePost
feed_models: list[Type[FeedItem]] = [
    Post,
    AppPost,
    ChangelogPost,
]


def get_feed(
    query: str | None = None, tag: str | None = None, **kwargs
) -> list[FeedItem]:
    def build_qs(model_class: Type[FeedItem]):
        qs = model_class.objects.published()

        if tag:
            qs = qs.filter(tags__name=tag)
        if query:
            qs = qs.search(query)
        return (
            qs.filter(**kwargs)
            .prefetch_related("related_files")
            .order_by("-published_at")
        )

    feed = list(chain(*(build_qs(x) for x in feed_models)))
    return sorted(feed, key=_sort_queryset, reverse=True)


def _sort_queryset(instance: FeedItem):
    return instance.published_at
