from typing import List

from common.models.search import SearchResult
from django.http import HttpRequest
from main.views.querysets import Feed, get_search_results, get_suggestions
from ninja import Router, Schema

router = Router()


class SearchResponseSchema(Schema):
    query: str
    feed: List[SearchResult]


@router.get("/", response=SearchResponseSchema)
def search(request: HttpRequest, query: str):
    results: Feed = get_search_results(query)
    return {
        "query": query,
        "feed": [x.to_search_result() for x in results],
    }


@router.get("/suggestions/", response=List[SearchResult])
def suggestions(request: HttpRequest):
    return get_suggestions()
