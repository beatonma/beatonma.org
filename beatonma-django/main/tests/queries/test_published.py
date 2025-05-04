from basetest.testcase import LocalTestCase
from main.models import Post
from main.tasks import sample_data


class PublishedMixinTests(LocalTestCase):
    def setUp(self):
        sample_data.create_post(content="public", is_published=True)
        sample_data.create_post(content="private", is_published=False)

    def test_searchability(self):
        self.assertEqual(1, Post.objects.search("public").count())
        self.assertEqual(0, Post.objects.search("private").count())
        self.assertEqual(1, Post.objects.search("p").count())
