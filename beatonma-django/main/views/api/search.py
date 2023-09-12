import dataclasses

from common.views.api import ApiView
from django.http import JsonResponse
from main.views.querysets import get_search_results, get_suggestions


class SearchSuggestionsView(ApiView):
    def get(self, request, *args, **kwargs):
        results = get_suggestions()

        return JsonResponse(
            {
                "suggestions": [dataclasses.asdict(x) for x in results],
            }
        )


class SearchApiView(ApiView):
    def get(self, request):
        query = request.GET.get("query", "")
        results = get_search_results(query)
        results = list(map(lambda x: x.to_search_result().to_json(), results))

        return JsonResponse({"query": query, "feed": results})
