from basetest.testcase import LocalTestCase
from django.core.exceptions import ValidationError
from main.models import AboutPost


class AboutTests(LocalTestCase):
    def root(self):
        return AboutPost.objects.root()

    def slug(self, slug: str):
        return AboutPost.objects.get(slug=slug)

    def setUp(self):
        root = AboutPost.objects.create(
            slug="overwritten_root_slug", content="This is the root page"
        )

        child = AboutPost.objects.create(
            parent=root, slug="child", content="This is a child page"
        )
        AboutPost.objects.create(
            parent=root, slug="sibling", content="This is a sibling page"
        )

        grandchild = AboutPost.objects.create(
            parent=child, slug="grandchild", content="This is a grandchild page"
        )

        previous = grandchild
        for n in range(5):
            previous = AboutPost.objects.create(
                parent=previous, slug=f"descendant_{n}", content=f"descendant #{n}"
            )

    def test_root_is_correct(self):
        self.assertEqual(self.root().slug, "root")
        self.assertEqual(self.root().content, "This is the root page")
        self.assertEqual(self.root().path, "")

    def test_root_is_required(self):
        root = self.root()
        root.parent = self.slug("child")
        with self.assertRaises(ValidationError):
            root.save()

    def test_single_root(self):
        with self.assertRaises(ValidationError):
            AboutPost.objects.create(content="This is another root page")

    def test_parent_cannot_be_self(self):
        child = self.slug("child")

        child.parent = child
        with self.assertRaises(ValidationError):
            child.save()

    def test_ancestor_loops_are_detected(self):
        grandchild = self.slug("grandchild")
        descendant_3 = self.slug("descendant_3")

        grandchild.parent = descendant_3
        with self.assertRaises(ValidationError):
            grandchild.save()

        grandchild.parent = grandchild.children.first()
        with self.assertRaises(ValidationError):
            grandchild.save()

    def test_path_is_correct(self):
        self.assertEqual(self.slug("child").path, "child/")

    def test_path_is_updated(self):
        child = self.slug("child")
        child.slug = "changed"
        child.save()

        self.assertEqual(self.slug("grandchild").path, "changed/grandchild/")
