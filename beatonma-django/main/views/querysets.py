import random
from dataclasses import dataclass
from itertools import chain
from typing import Callable, List, Optional, Type

from common.models import PublishedMixin
from common.models.published import PublishedQuerySet
from common.models.search import SearchResult
from common.models.util import implementations_of
from django.conf import settings
from django.db.models import QuerySet
from github.models import GithubLanguage, GithubRepository
from main.models import App, AppType, Article, Blog, Changelog, Note
from main.views import reverse
from main.views.util import pluralize
from taggit.models import Tag

Feed = List[PublishedMixin]

_searchable_models: List[PublishedMixin] = list(
    filter(lambda Model: Model.search_enabled, implementations_of(PublishedMixin))
)


def get_main_feed() -> Feed:
    return _build_feed()


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

    return _sorted_feed(_flatten(apps, repos)) + private_repos


def get_search_results(query: str) -> Feed:
    if not query:
        return []

    return _build_feed(lambda qs: qs.search(query))


def get_suggestions(
    tags: bool = True,
    app_types: bool = True,
    languages: bool = True,
) -> List[SearchResult]:
    _tags = (
        [
            SearchResult(
                name=f"#{tag.name}",
                url=reverse.tag(tag),
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
            )
            for language in get_languages()
        ]
        if languages
        else []
    )

    results = _tags + _app_types + _languages
    random.shuffle(results)

    return results[: settings.SEARCH_MAX_SUGGESTIONS]


def get_apps(**filter_kwargs) -> PublishedQuerySet[App]:
    return App.objects.published().filter(**filter_kwargs)


def get_articles(**filter_kwargs) -> PublishedQuerySet[Article]:
    return Article.objects.published().filter(**filter_kwargs)


def get_blogs(**filter_kwargs) -> PublishedQuerySet[Blog]:
    return Blog.objects.published().filter(**filter_kwargs)


def get_changelogs(**filter_kwargs) -> PublishedQuerySet[Changelog]:
    return Changelog.objects.published().filter(**filter_kwargs)


def get_notes(**filter_kwargs) -> PublishedQuerySet[Note]:
    return Note.objects.published().filter(**filter_kwargs)


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
    if queryset_method:
        results = [queryset_method(M.objects.published()) for M in _searchable_models]

    else:
        results = [M.objects.published().filter(**kwargs) for M in _searchable_models]

    return _sorted_feed(_flatten(*results))


def _sorted_feed(items: Feed) -> Feed:
    def sort_key(item: PublishedMixin):
        return item.get_sorting_datetime()

    return sorted(items, key=sort_key, reverse=True)


def _flatten(*querysets) -> Feed:
    """Unpack querysets into flat list of the items from those querysets."""
    return list(chain(*querysets))


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
