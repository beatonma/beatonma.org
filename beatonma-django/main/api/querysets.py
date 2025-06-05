import logging

from django.db.models import Case, CharField, QuerySet, Value, When
from main.models.posts.post import Post

log = logging.getLogger(__name__)


type FeedItem = Post


def get_feed_filters(params: dict) -> dict:
    return {key: params.get(key) for key in ["query", "tag", "feed"]}


def get_feed(
    *,
    query: str | None = None,
    tag: str | None = None,
    feed: str | None = None,
) -> QuerySet[FeedItem]:
    qs: QuerySet[FeedItem] = Post.objects.published()

    if feed:
        qs = qs.filter(feeds__slug=feed)
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
