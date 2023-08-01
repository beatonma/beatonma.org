import random
from dataclasses import dataclass
from itertools import chain
from typing import Callable, List, Optional, Type

from common.models import PublishedMixin
from common.models.search import SearchResult
from common.models.util import implementations_of
from django.db.models import QuerySet
from github.models import GithubLanguage, GithubRepository
from main.models import App, AppType, Article, Blog, Changelog, Note
from main.views import reverse
from taggit.models import Tag

MAX_SUGGESTIONS = 10


def _sorted_feed(items: List[PublishedMixin]) -> List[PublishedMixin]:
    return sorted(items, key=lambda x: x.get_sorting_datetime(), reverse=True)


def get_main_feed() -> List[PublishedMixin]:
    feed = _build_feed(lambda m: m.objects.published())

    return _sorted_feed(feed)


def get_search_results(query: str, to_json: bool = False) -> dict:
    if not query:
        return dict(
            query=query,
            feed=[],
        )

    feed = _build_feed(lambda m: m.objects.search(query))

    if to_json:
        feed = list(map(lambda x: x.to_search_result().to_json(), feed))

    return {
        "query": query,
        "feed": feed,
    }


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

    return results


def get_apps(**filter_kwargs) -> QuerySet[App]:
    return App.objects.published().filter(**filter_kwargs)


def get_articles(**filter_kwargs) -> QuerySet[Article]:
    return Article.objects.published().filter(**filter_kwargs)


def get_blogs(**filter_kwargs) -> QuerySet[Blog]:
    return Blog.objects.published().filter(**filter_kwargs)


def get_changelogs(**filter_kwargs) -> QuerySet[Changelog]:
    return Changelog.objects.published().filter(**filter_kwargs)


def get_notes(**filter_kwargs) -> QuerySet[Note]:
    return Note.objects.published().filter(**filter_kwargs)


def get_app_types(**filter_kwargs) -> QuerySet[AppType]:
    return AppType.objects.filter(**filter_kwargs)


def get_tags(**filter_kwargs) -> QuerySet[Tag]:
    return Tag.objects.filter(**filter_kwargs)


def get_repositories(**filter_kwargs) -> QuerySet[GithubRepository]:
    return GithubRepository.objects.published().filter(**filter_kwargs)


def get_languages(**filter_kwargs) -> QuerySet[GithubLanguage]:
    return GithubLanguage.objects.filter(**filter_kwargs)


@dataclass
class FeedMessage:
    """A message that appears in a feed without being attached to any objects."""

    message: Optional[str]
    url: Optional[str] = None


def _build_feed(
    query: Callable[[Type], QuerySet],
):
    _models = filter(lambda x: x.search_enabled, implementations_of(PublishedMixin))

    results = list(chain(*[query(M) for M in _models]))
    return _sorted_feed(results)
