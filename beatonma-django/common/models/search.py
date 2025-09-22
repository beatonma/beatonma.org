import operator
import re
from functools import reduce
from typing import Callable

from django.db import connection, models
from django.db.models import Q, QuerySet

_DB_VENDOR = connection.vendor
_WORD_BOUNDARY_REGEX = {
    "sqlite": r"\b",
    "postgresql": r"\y",
}.get(_DB_VENDOR, r"\b")

QUERY_MAX_LENGTH = 64
QUERY_MAX_WORDS = 5


class SearchQuerySet(QuerySet):
    def __init__(self, *args, distinct: bool = None, **kwargs):
        super().__init__(*args, **kwargs)

        self._search_enabled = getattr(self.model, "search_enabled", True)
        if not self._search_enabled:
            return

        self._search_fields = self.model.search_fields
        if distinct is None:
            self._distinct = bool([x for x in self._search_fields if "__" in x])
        else:
            self._distinct = distinct

    def search(self, query: str) -> QuerySet:
        if not self._search_enabled or not self._search_fields:
            return self.none()

        words = self._parse_words(query)
        word_results = self._search_words(words)

        if word_results.exists():
            return word_results

        return self._search_anything(words)

    @staticmethod
    def _parse_words(query: str) -> list[str]:
        query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
        query = query[:QUERY_MAX_LENGTH]
        words = query.strip().split()
        words = [re.escape(word) for word in words]

        return words[:QUERY_MAX_WORDS]

    def _build_search_filter(
        self,
        words: list[str],
        fields: list[str],
        filter_suffix: str,
        field_join: Callable,
        overall_join: Callable,
    ) -> QuerySet:
        filters = [
            reduce(
                lambda q, word: field_join(q, Q(**{f"{field}{filter_suffix}": word})),
                words,
                Q(),
            )
            for field in fields
        ]

        q_filter = reduce(overall_join, filters, Q())

        return self._apply_distinct(self.filter(q_filter))

    def _search_words(self, words: list[str]) -> QuerySet:
        """Filter for any fields that match all the words in the query.

        A match is a whole word: 'sample' will not match 'samples'."""
        return self._build_search_filter(
            [rf"{_WORD_BOUNDARY_REGEX}{word}{_WORD_BOUNDARY_REGEX}" for word in words],
            self._search_fields,
            "__iregex",
            operator.and_,
            operator.or_,
        )

    def _search_fragments(self, words: list[str]) -> QuerySet:
        """Filter for any fields that contain all the word fragments in query.

        This is more lenient than _search_words: 'sample' will match 'samples'."""

        return self._build_search_filter(
            words, self._search_fields, "__icontains", operator.and_, operator.or_
        )

    def _search_anything(self, words: list[str]) -> QuerySet:
        """Filter for any word matching any field."""
        return self._build_search_filter(
            words, self._search_fields, "__icontains", operator.or_, operator.or_
        )

    def _apply_distinct(self, qs: QuerySet) -> QuerySet:
        if self._distinct:
            return qs.distinct()
        return qs


class SearchMixin(models.Model):
    class Meta:
        abstract = True

    search_enabled: bool = True
    search_fields: list[str]

    queryset_class = SearchQuerySet
