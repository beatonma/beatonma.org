import random
from dataclasses import dataclass
from itertools import chain
from typing import Callable, Dict, List, Optional, Type

from common.models import PublishedMixin
from common.models.published import PublishedQuerySet
from common.models.search import SearchResult
from common.models.util import implementations_of
from django.conf import settings
from django.db.models import QuerySet
from github.models import GithubLanguage, GithubRepository
from main.models import App, AppType, Article, Changelog
from main.views import reverse
from main.views.util import pluralize
from taggit.models import Tag

type Feed = List[PublishedMixin]

_searchable_models: List[Type[PublishedMixin]] = list(
    filter(lambda Model: Model.search_enabled, implementations_of(PublishedMixin))
)

_prefetch_fields: Dict[Type[PublishedMixin], List[str]] = {
    Model: ["related_files"]
    for Model in _searchable_models
    if hasattr(Model, "related_files")
}
_prefetch_fields[Article] += ["apps"]
_select_fields: Dict[Type[PublishedMixin], List[str]] = {
    Changelog: ["app"],
}


def get_main_feed() -> Feed:
    return _build_feed()


def get_apps_feed(app_type: Optional[str] = None) -> Feed:
    if app_type:
        apps = get_apps(app_type__name__iexact=app_type)
    else:
        apps = get_apps()

    return _build_feed_from(apps)


def get_for_tag(tag: str) -> Feed:
    query = {"tags__name__iexact": tag}
    return _build_feed(**query) + _get_private_repos_result(**query)


def get_for_language(language: str) -> Feed:
    resolved_language = (
        GithubLanguage.objects.filter(name__iexact=language).first()
        or GithubLanguage.objects.filter(name__icontains=language).first()
    )
    if not resolved_language:
        return []

    apps = get_apps(primary_language=resolved_language)
    repos = get_repositories(primary_language=resolved_language)
    private_repos = _get_private_repos_result(primary_language=resolved_language)

    return _build_feed_from(apps, repos) + private_repos


def get_search_results(query: str) -> Feed:
    if not query:
        return []

    return _build_feed(lambda qs: qs.search(query))


def get_suggestions(
    tags: bool = False,
    app_types: bool = False,
    languages: bool = False,
) -> List[SearchResult]:
    if tags is app_types is languages is False:
        # If no types are specified, default to all.
        tags = app_types = languages = True

    _tags = (
        [
            SearchResult(
                name=tag.name,
                url=reverse.tag(tag),
                className="tag",
            )
            for tag in get_tags()
        ]
        if tags
        else []
    )
    _app_types = (
        [
            SearchResult(
                name=apptype.name,
                url=apptype.get_absolute_url(),
            )
            for apptype in get_app_types()
        ]
        if app_types
        else []
    )
    _languages = (
        [
            SearchResult(
                name=language.name,
                url=reverse.language(language),
                className="language",
            )
            for language in get_languages()
        ]
        if languages
        else []
    )

    results = _tags + _app_types + _languages
    random.shuffle(results)

    return results[: settings.BMA_SEARCH_MAX_SUGGESTIONS]


def get_apps(**filter_kwargs) -> PublishedQuerySet[App]:
    return App.objects.published().filter(**filter_kwargs)


def get_app_types(**filter_kwargs) -> QuerySet[AppType]:
    return AppType.objects.filter(**filter_kwargs)


def get_tags(**filter_kwargs) -> QuerySet[Tag]:
    return Tag.objects.filter(**filter_kwargs)


def get_repositories(**filter_kwargs) -> PublishedQuerySet[GithubRepository]:
    return GithubRepository.objects.published().filter(**filter_kwargs)


def get_languages(**filter_kwargs) -> QuerySet[GithubLanguage]:
    return GithubLanguage.objects.filter(**filter_kwargs)


def _build_feed(
    queryset_method: Callable[[Type[PublishedQuerySet]], QuerySet] = None,
    **kwargs,
) -> Feed:
    def _query(M):
        qs = M.objects.published().filter(**kwargs)

        if prefetch_fields := _prefetch_fields.get(M):
            qs = qs.prefetch_related(*prefetch_fields)

        if select_fields := _select_fields.get(M):
            qs = qs.select_related(*select_fields)

        return qs.order_by("-published_at")

    if queryset_method:
        results = [queryset_method(_query(M)) for M in _searchable_models]

    else:
        results = [_query(M) for M in _searchable_models]

    return _build_feed_from(*results)


def _build_feed_from(*querysets: PublishedQuerySet) -> Feed:
    flat_feed = [x for x in chain(*querysets) if x.is_publishable()]

    def sort_key(item: PublishedMixin):
        return item.get_sorting_datetime()

    return sorted(flat_feed, key=sort_key, reverse=True)


@dataclass
class FeedMessage:
    """A message that appears in a feed without being attached to any objects."""

    message: Optional[str]
    url: Optional[str] = None


def _get_private_repos_result(**query) -> List[FeedMessage]:
    private_repos_count = GithubRepository.objects.get_private_count(**query)

    if private_repos_count == 0:
        return []

    return [
        FeedMessage(
            message=f"{private_repos_count} private "
            f"{pluralize(private_repos_count, 'repository', 'repositories')}",
        )
    ]
