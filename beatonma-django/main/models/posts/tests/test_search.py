from basetest.testcase import LocalTestCase
from main.models import Post
from main.tasks import sample_data


def _search(query: str):
    return Post.objects.search(query)


class SearchQueryTests(LocalTestCase):
    def _assert_results(self, query: str, n: int, func=_search):
        self.assert_length(func(query), n, msg=f"query:{query}")

    def setUp(self) -> None:
        sample_data.create_post(
            title=None,
            content="The Basics of Photography: Learn the fundamentals of "
            "photography and how to capture stunning images. Also chickens.",
            tags=["apples"],
        )

        sample_data.create_post(
            title=None,
            content="Photography Basics: Learn the fundamentals of photography "
            "and how to capture stunning images. Also turkeys.",
            tags=["oranges"],
        )
        sample_data.create_post(title=None, content="public", is_published=True)
        sample_data.create_post(title=None, content="private", is_published=False)


class FullSearchTests(SearchQueryTests):
    def test_search_word_order_is_agnostic(self):
        self._assert_results("photography basics", 2)
        self._assert_results("basic photography", 2)

    def test_search_single_word(self):
        self._assert_results("chickens", 1)
        self._assert_results("turkeys", 1)
        self._assert_results("ducks", 0)

    def test_search_multiple_fields(self):
        self._assert_results("chickens apples", 1)
        self._assert_results("chickens oranges", 2)
        self._assert_results("turkey apples", 2)
        self._assert_results("turkey orange", 1)
        self._assert_results("oran", 1)


class PrivateSearchTests(SearchQueryTests):
    def test_private_posts_not_searchable(self):
        self._assert_results("public", 1)
        self._assert_results("private", 0)
        self._assert_results("p", 3)


class QueryEscapeTests(SearchQueryTests):
    def test_sanitization(self):
        self._assert_results("((Also ducks)", 2)
        self._assert_results("'Also ducks", 2)
        self._assert_results("'Also ducks\"", 2)
        self._assert_results("HLxv))%2C).%2C%2C)%27%22", 0)
