from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ApiPagination(LimitOffsetPagination):
    max_limit = 50

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_offset()),
                    ("next_url", self.get_next_link()),
                    ("previous", self.get_previous_offset()),
                    ("previous_url", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )

    def get_next_offset(self) -> int | None:
        next_offset = self.offset + self.limit
        if next_offset >= self.count:
            return None
        return next_offset

    def get_previous_offset(self) -> int | None:
        if self.offset <= 0:
            return None

        offset = self.offset - self.limit
        return max(0, offset)
