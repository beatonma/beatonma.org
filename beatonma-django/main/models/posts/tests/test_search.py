from basetest.testcase import LocalTestCase
from main.models import Post
from main.tasks import sample_data


def _words(query: str):
    words = query.strip().split()
    return Post.objects.search_words(words)


def _fragments(query: str):
    words = query.strip().split()
    return Post.objects.search_fragments(words)


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


class PartialSearchTests(SearchQueryTests):
    def test_search_all_words_required(self):
        self._assert_results("photography basics chickens", 1, _words)
        self._assert_results("turkeys basics photography", 1, _words)
        self._assert_results("photography chickens basics capture learn", 1, _words)
        self._assert_results("photography basics champagne chickens", 0, _words)
        self._assert_results("photography turkey basics chickens", 0, _words)

    def test_search_word_fragments(self):
        self._assert_results("chick", 1, _fragments)
        self._assert_results("duck", 0, _fragments)
        self._assert_results("basic photo fundamental", 2, _fragments)
        self._assert_results("basic photo ducks", 0, _fragments)


class FullSearchTests(SearchQueryTests):
    def test_search_word_order_is_agnostic(self):
        self._assert_results("photography basics", 2)

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
