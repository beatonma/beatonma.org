import logging

from django.db.models import Case, CharField, QuerySet, Value, When

from main.models.posts.feed import FeedsMixin
from main.models.posts.post import Post

log = logging.getLogger(__name__)


def get_feed_filters(params: dict) -> dict:
    return {key: params.get(key) for key in ["query", "tag", "feed"]}


def get_feed(
    *,
    query: str | None = None,
    tag: str | None = None,
    feed: str | None = None,
) -> QuerySet[Post]:
    qs = Post.objects.published()

    if feed:
        qs = qs.filter(feeds__slug=feed)
    else:
        # If a feed is not specified, default to main 'posts' feed.
        qs = qs.filter(feeds__slug=Post.DEFAULT_FEED_SLUG)

    if query:
        qs = qs.search(query)
    if tag:
        qs = qs.filter(tags__name=tag)

    qs = (
        qs.annotate(
            post_type=Case(
                When(apppost__id__isnull=False, then=Value("app")),
                When(changelogpost__id__isnull=False, then=Value("changelog")),
                default=Value("post"),
                output_field=CharField(),
            )
        )
        .prefetch_related("related_files")
        .select_related("apppost", "changelogpost")
    ).distinct()

    return qs.order_by("-published_at")
