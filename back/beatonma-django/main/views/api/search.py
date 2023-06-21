import dataclasses

from common.views.api import ApiView
from django.http import JsonResponse
from main.views.querysets import MAX_SUGGESTIONS, get_search_results, get_suggestions


class SearchSuggestionsView(ApiView):
    def get(self, request, *args, **kwargs):
        results = get_suggestions()

        return JsonResponse(
            dict(suggestions=[dataclasses.asdict(x) for x in results[:MAX_SUGGESTIONS]])
        )


class SearchApiView(ApiView):
    def get(self, request):
        query = request.GET.get("query", "")
        return JsonResponse(get_search_results(query, to_json=True))
