import dataclasses
from dataclasses import dataclass
from typing import Dict, Iterable

from django.conf import settings
from django.core.paginator import Page, Paginator
from django.http import HttpRequest


@dataclass
class Paginated:
    page_obj: Page
    page: int = dataclasses.field(init=False)
    feed: Iterable = dataclasses.field(init=False)
    is_first_page: bool = dataclasses.field(init=False)

    def __post_init__(self):
        self.page = self.page_obj.number
        self.feed = self.page_obj.object_list
        self.is_first_page = self.page == 1

    def as_context(self) -> Dict:
        return {
            "page_obj": self.page_obj,
            "page": self.page,
            "feed": self.feed,
            "is_first_page": self.is_first_page,
        }


def paginate(request: HttpRequest, items: Iterable) -> Paginated:
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    paginator = Paginator(items, settings.BMA_FEED_ITEMS_PER_PAGE)
    page = paginator.get_page(page)

    return Paginated(page_obj=page)
