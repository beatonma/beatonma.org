from typing import Dict, Iterable

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest


def paginate(request: HttpRequest, items: Iterable) -> Dict:
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    paginator = Paginator(items, settings.BMA_FEED_ITEMS_PER_PAGE)
    page = paginator.get_page(page)

    return {
        "page_obj": page,
        "page": page.number,
        "feed": page.object_list,
        "is_first_page": page.number == 1,
    }
