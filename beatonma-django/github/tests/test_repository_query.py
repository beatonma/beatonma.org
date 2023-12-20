from basetest.testcase import LocalTestCase
from github.management.commands.sample_github_data import create_sample_repository
from github.models import GithubRepository


class GithubRepositoryQueryTest(LocalTestCase):
    def setUp(self):
        create_sample_repository(
            name="private public",
            is_private=True,
            is_published=True,
        )
        create_sample_repository(
            name="public public",
            is_private=False,
            is_published=True,
        )
        create_sample_repository(
            name="private private",
            is_private=True,
            is_published=False,
        )
        create_sample_repository(
            name="public private",
            is_private=False,
            is_published=False,
        )

    def test_repository_query(self):
        published = GithubRepository.objects.published()

        self.assert_length(published, 1)
        self.assertEqual(published.first().name, "public public")
