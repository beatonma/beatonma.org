import logging

from django.db.models import Case, CharField, QuerySet, Value, When
from main.models import Post
from main.models.posts.post import BasePost

log = logging.getLogger(__name__)


type FeedItem = BasePost


def get_feed(
    *,
    query: str | None = None,
    tag: str | None = None,
    **kwargs,
) -> QuerySet[FeedItem]:
    qs = Post.objects.published().filter(**kwargs)

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
