from basetest.testcase import SimpleTestCase
from main.api.schema import HexColor, HtmlAttribute, Url, UrlSearchParams
from ninja import Schema
from pydantic import ValidationError


class SchemaTests(SimpleTestCase):
    def test_HexColor(self):
        class Foo(Schema):
            color: HexColor

        self.assertEqual(Foo.model_validate({"color": "#ff0000"}).color, "#ff0000")
        self.assertEqual(Foo.model_validate({"color": "#AABBCC"}).color, "#AABBCC")
        self.assertIsNone(Foo.model_validate({"color": "#ff000"}).color)

    def test_Url(self):
        class Foo(Schema):
            url: Url

        self.assertEqual(
            Foo.model_validate({"url": "https://example.com"}).url,
            "https://example.com",
        )
        self.assertEqual(
            Foo.model_validate({"url": "https://example.com/test"}).url,
            "https://example.com/test",
        )
        self.assertEqual(
            Foo.model_validate({"url": "/test"}).url,
            "/test",
        )

        with self.assertRaises(ValidationError):
            Foo.model_validate({"url": "test"})

        with self.assertRaises(ValidationError):
            Foo.model_validate({"url": "a/b/test"})

    def test_HtmlAttribute(self):
        class Foo(Schema):
            attr: HtmlAttribute

        self.assertEqual(Foo.model_validate({"attr": "<html>"}).attr, "&lt;html&gt;")
        self.assertEqual(Foo.model_validate({"attr": 'value"'}).attr, "value&quot;")
        self.assertEqual(
            Foo.model_validate({"attr": "background: #ff0000;"}).attr,
            "background: #ff0000;",
        )

    def test_UrlSearchParams(self):
        class Foo(Schema):
            params: UrlSearchParams

        self.assertEqual(
            Foo.model_validate({"params": "a=1&b=2&3=abc"}).params, "a=1&b=2&3=abc"
        )
        self.assertEqual(Foo.model_validate({"params": "one two"}).params, "one%20two")
