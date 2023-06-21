from basetest.testcase import LocalTestCase
from main.models import Note


class PublishedMixinTests(LocalTestCase):
    def setUp(self) -> None:
        Note.objects.create(content="public", is_published=True)
        Note.objects.create(content="private", is_published=False)

    def test_unpublished_content_is_not_accessible(self):
        self.assert_exists(Note, count=1)
        self.assertIsNone(Note.objects.filter(content="private").first())
        with self.assertRaises(Note.DoesNotExist):
            self.assertIsNone(Note.objects.get(content="private"))

        Note.objects.get(content="public")
