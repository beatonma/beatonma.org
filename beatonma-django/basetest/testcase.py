import sys
from typing import Optional, Sized, Type, Union
from unittest import skipIf

import pytest
from common.models.types import Model
from common.util.html import find_links_in_soup, html_parser
from django.db.models import QuerySet
from django.test import TestCase


class BaseTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def teardown_models(self, *models):
        for M in models:
            M.objects.all().delete()

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

    def assert_exists(
        self,
        model_class: Type[Model],
        count: int = 1,
        **query,
    ) -> Union[Model, QuerySet[Model]]:
        """Assert that the expected number of model instances exist and return it/them."""

        qs: QuerySet[Model]
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

    def assert_length(self, items: Sized, expected: int, msg: Optional[str] = ""):
        self.assertEqual(
            len(items),
            expected,
            msg=f"Expected {expected} items, got {(len(items))}: {items} {msg}",
        )

    def assert_html_links_to(
        self,
        html: str,
        href: str,
        displaytext: Optional[str] = None,
    ):
        soup = html_parser(html)
        links = {(a["href"], a.get_text(strip=True)) for a in find_links_in_soup(soup)}

        if displaytext:
            results = [x for x in links if x[0] == href and x[1] == displaytext]
            self.assertTrue(
                len(results) > 0,
                msg=f"Link (href='{href}', text='{displaytext}') not found in {links}",
            )

        else:
            results = set(filter(lambda x: x[0] == href, links))
            self.assertTrue(
                len(results) > 0,
                msg=f"Link {href} not found in {[x[0] for x in links]}",
            )


class LocalTestCase(BaseTestCase):
    """Tests that use only local data - no external network calls!"""

    pass


@pytest.mark.skipif("config.getoption('notemplate')")
class TemplateTestCase(LocalTestCase):
    """Tests that require templates to be available."""

    pass


@pytest.mark.skipif("not config.getoption('network')")
@skipIf(
    "manage.py" in sys.argv,
    reason="Use `pytest --network` to run tests from NetworkTestCase.",
)
class NetworkTestCase(BaseTestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via `pytest--network`.
    """

    pass
