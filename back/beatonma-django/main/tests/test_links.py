from basetest.testcase import LocalTestCase
from django.contrib.contenttypes.models import ContentType
from main.models import Host, Link, Note


class LinkTests(LocalTestCase):
    def test_link_parsing(self):
        """Link model correctly creates instances of Host."""
        links_string = [
            "https://beatonma.org",
            "snommoc.org",
            "https://inverness.io/",
            "https://inverness.io/sample/",
        ]

        target = Note.objects.create(
            content="Hello",
        )

        for url in links_string:
            Link.objects.create(
                url=url,
                object_id=target.pk,
                content_type=ContentType.objects.get_for_model(target),
            )

        hosts = Host.objects.all()
        self.assertEqual(hosts.count(), 3)
        hosts.get(domain="beatonma.org")
        hosts.get(domain="snommoc.org")
        hosts.get(domain="inverness.io")

    def tearDown(self) -> None:
        self.teardown_models(
            Link,
            Host,
        )
