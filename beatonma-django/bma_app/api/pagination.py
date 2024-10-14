from typing import Any, List

from django.conf import settings
from django.db.models import QuerySet
from ninja import Schema
from ninja.pagination import PaginationBase


class OffsetPagination(PaginationBase):
    page_size: int = settings.BMA_FEED_ITEMS_PER_PAGE
    items_attribute: str = "results"

    class Input(Schema):
        offset: int = 0

    class Output(Schema):
        results: List[Any]
        count: int
        next: int | None
        previous: int | None

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        count = queryset.count()
        offset = pagination.offset

        def get_next_offset():
            next_offset = offset + self.page_size
            if next_offset >= count:
                next_offset = None
            return next_offset

        def get_previous_offset():
            if offset <= 0:
                return None
            return max(0, offset - self.page_size)

        return {
            "count": count,
            "next": get_next_offset(),
            "previous": get_previous_offset(),
            "results": queryset[offset : offset + self.page_size],
        }
