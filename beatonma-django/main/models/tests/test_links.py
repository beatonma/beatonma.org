from basetest.testcase import LocalTestCase
from common.models.generic import generic_fk
from main.models import Host, Link
from main.tasks import sample_data


class LinkTests(LocalTestCase):
    def test_link_parsing(self):
        """Link model correctly creates instances of Host."""
        links_string = [
            "https://beatonma.org",
            "snommoc.org",
            "https://inverness.io/",
            "https://inverness.io/sample/",
        ]

        target = sample_data.create_post(content="Hello")

        for url in links_string:
            Link.objects.create(url=url, **generic_fk(target))

        hosts = Host.objects.all()
        self.assertEqual(hosts.count(), 3)
        hosts.get(domain="beatonma.org")
        hosts.get(domain="snommoc.org")
        hosts.get(domain="inverness.io")
