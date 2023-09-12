import logging
import random
from typing import Iterable, List, Optional, Union

from common.models import SearchMixin
from common.models.search import SearchResult
from common.views.logged import LoggedView
from django.db.models import QuerySet
from django.shortcuts import redirect, render
from main.views import view_names
from main.views.querysets import (
    get_app_types,
    get_apps,
    get_for_language,
    get_for_tag,
    get_languages,
    get_search_results,
    get_suggestions,
)
from main.views.util.pagination import paginate
from taggit.models import Tag

log = logging.getLogger(__name__)


class SearchView(LoggedView):
    def get(self, request):
        query = request.GET.get("query")
        if not query:
            return redirect(view_names.INDEX)

        if query[:1] == "#":
            return redirect(view_names.TAGS, tag=query[1:])

        return _render_results(
            request,
            "pages/search/search.html",
            search_query=query,
            results=get_search_results(query),
            filters=get_suggestions(),
        )


class TagView(LoggedView):
    def get(self, request, tag: str):
        results = get_for_tag(tag)
        filters = _get_random_filters(Tag.objects.all())

        return _render_results(
            request,
            "pages/search/tag.html",
            search_query=tag,
            results=results,
            filters=filters,
        )


class LanguageView(LoggedView):
    def get(self, request, language: str):
        results = get_for_language(language)
        filters = _get_random_filters(get_languages())

        return _render_results(
            request,
            "pages/search/language.html",
            search_query=language,
            results=results,
            filters=filters,
        )


class AllAppsView(LoggedView):
    def get(self, request):
        results = get_apps().sort_by_recent()
        filters = _get_random_filters(get_app_types())

        return _render_results(
            request,
            "pages/search/apps.html",
            search_query="",
            results=results,
            filters=filters,
        )


class FilteredAppsView(LoggedView):
    def get(self, request, app_type: str):
        results = get_apps().filter(app_type__name__iexact=app_type).sort_by_recent()
        filters = _get_random_filters(get_app_types())

        return _render_results(
            request,
            "pages/search/apps.html",
            search_query=app_type,
            results=results,
            filters=filters,
        )


def _render_results(
    request,
    template_name: str,
    search_query: str,
    results: Iterable[SearchMixin],
    filters: Optional[List[Union[str, SearchResult]]] = None,
):
    paginated_context = paginate(request, results).as_context()

    return render(
        request,
        template_name,
        context={
            "filter": search_query,
            "filters": filters or [],
            **paginated_context,
        },
    )


def _get_random_filters(qs: QuerySet, field_name: str = "name"):
    result = list(qs.values_list(field_name, flat=True))
    random.shuffle(result)
    return result
