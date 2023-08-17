from basetest.testcase import LocalTestCase
from main.models import Note


class PublishedMixinTests(LocalTestCase):
    def setUp(self):
        Note.objects.create(id=1, content="public", is_published=True)
        Note.objects.create(id=2, content="private", is_published=False)

    def test_searchability(self):
        self.assertEqual(1, Note.objects.search("public").count())
        self.assertEqual(0, Note.objects.search("private").count())
        self.assertEqual(1, Note.objects.search("p").count())
