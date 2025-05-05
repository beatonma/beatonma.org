import sys
from pathlib import Path
from typing import Iterable, Sized, Type
from unittest import skipIf

import pytest
from common.util.html import html_parser
from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.test import SimpleTestCase as DjangoSimpleTestCase
from django.test import TestCase

__all__ = ["SimpleTestCase", "LocalTestCase", "NetworkTestCase"]


class SimpleTestCase(DjangoSimpleTestCase):
    maxDiff = None

    def assert_length(self, items: Sized, expected: int, msg: str = ""):
        self.assertEqual(
            len(items),
            expected,
            msg=f"Expected {expected} items, got {(len(items))}: {items} {msg}",
        )

    def assert_html_links_to(
        self,
        html: str,
        href: str | Iterable[str],
        displaytext: str = None,
    ):
        if isinstance(href, list) or isinstance(href, set):
            for url in href:
                self.assert_html_links_to(html, url, displaytext)
            return

        soup = html_parser(html)
        links = {
            (a["href"], a.get_text(strip=True)) for a in soup.find_all("a", href=True)
        }
        if not links:
            raise AssertionError(f"No links found in HTML: {html}")

        if displaytext:
            results = [x for x in links if x[0] == href and x[1] == displaytext]
            formatted_links = "\n- ".join([str(x) for x in links])
            self.assertTrue(
                len(results) > 0,
                msg=f"Link (href='{href}', text='{displaytext}') not found in: \n- {formatted_links}",
            )

        else:
            results = set(filter(lambda x: x[0] == href, links))
            formatted_links = "\n- ".join([x[0] for x in links])
            self.assertTrue(
                len(results) > 0,
                msg=f"Link {href} not found in: \n- {formatted_links}",
            )

    @staticmethod
    def relpath(location: str, path: str) -> Path:
        """Resolve `path` relative to `location`.
        `location` should usually be the value of `__file__` in the calling module"""
        return Path(location).parent.relative_to(settings.BASE_DIR) / path


class DatabaseTestCase(SimpleTestCase, TestCase):
    def assert_status(
        self,
        url_path: str,
        status_code: int = 200,
    ):
        response = self.client.get(url_path)

        self.assertEqual(response.status_code, status_code)

    def assert_status_ok(self, url_path: str):
        self.assert_status(
            url_path,
            status_code=200,
        )

    def assert_has_content(self, url_path: str, *content: str, status_code: int = 200):
        response = self.client.get(url_path)

        self.assertEqual(response.status_code, status_code)

        for text in content:
            self.assertContains(response, text)

    def assert_exists[
        T: models.Model
    ](self, model_class: Type[T], count: int = 1, **query,) -> T | QuerySet[T]:
        """Assert that the expected number of model instances exist and return it/them."""

        qs: QuerySet[T]
        if query:
            qs = model_class.objects.filter(**query)
        else:
            qs = model_class.objects.all()

        qs_count = qs.count()
        self.assertEqual(
            count,
            qs_count,
            msg=f"Expected {count} instance(s) of {model_class.__name__}, found {qs_count}.",
        )

        if count == 1:
            return qs.first()
        return qs


class LocalTestCase(DatabaseTestCase):
    """Tests that use only local data - no external network calls!"""

    pass


@pytest.mark.skipif("not config.getoption('network')")
@skipIf(
    "manage.py" in sys.argv,
    reason="Use `pytest --network` to run tests from NetworkTestCase.",
)
class NetworkTestCase(DatabaseTestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via `pytest--network`.
    """

    pass
