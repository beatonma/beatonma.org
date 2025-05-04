import operator
from functools import reduce
from typing import Callable

from django.db import connection, models
from django.db.models import Q, QuerySet

_DB_VENDOR = connection.vendor
_WORD_BOUNDARY_REGEX = {
    "sqlite": r"\b",
    "postgresql": r"\y",
}.get(_DB_VENDOR, r"\b")


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

        words = query.strip().split()

        word_results = self.search_words(words)

        if word_results.exists():
            return word_results

        return self.search_anything(words)

    def build_search_filter(
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

    def search_words(self, words: list[str]) -> QuerySet:
        """Filter for any fields that match all the words in the query.

        A match is a whole word: 'sample' will not match 'samples'."""
        return self.build_search_filter(
            [f"{_WORD_BOUNDARY_REGEX}{word}{_WORD_BOUNDARY_REGEX}" for word in words],
            self._search_fields,
            "__iregex",
            operator.and_,
            operator.or_,
        )

    def search_fragments(self, words: list[str]) -> QuerySet:
        """Filter for any fields that contain all the word fragments in query.

        This is more lenient than _search_words: 'sample' will match 'samples'."""

        return self.build_search_filter(
            words, self._search_fields, "__icontains", operator.and_, operator.or_
        )

    def search_anything(self, words: list[str]) -> QuerySet:
        """Filter for any word matching any field."""
        return self.build_search_filter(
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

    objects = SearchQuerySet.as_manager()
