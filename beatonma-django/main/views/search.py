import logging
from typing import Iterable, List, Optional, Union

from common.models import SearchMixin
from common.models.search import SearchResult
from common.views.logged import LoggedView
from django.shortcuts import redirect, render
from main.views import view_names
from main.views.querysets import (
    get_apps_feed,
    get_for_language,
    get_for_tag,
    get_search_results,
    get_suggestions,
)
from main.views.util.pagination import paginate

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
        filters = get_suggestions(tags=True)

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
        filters = get_suggestions(languages=True)

        return _render_results(
            request,
            "pages/search/language.html",
            search_query=language,
            results=results,
            filters=filters,
        )


class AllAppsView(LoggedView):
    def get(self, request):
        results = get_apps_feed()
        filters = get_suggestions(app_types=True)

        return _render_results(
            request,
            "pages/search/apps.html",
            search_query="",
            results=results,
            filters=filters,
        )


class FilteredAppsView(LoggedView):
    def get(self, request, app_type: str):
        results = get_apps_feed(app_type)
        filters = get_suggestions(app_types=True)

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
