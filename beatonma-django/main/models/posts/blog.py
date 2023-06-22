from django.urls import reverse
from main.models.mixins.themeable import ThemeableMixin
from main.models.posts.webpost import RichWebPost
from main.views import view_names


class Blog(ThemeableMixin, RichWebPost):
    """An informal post."""

    def get_absolute_url(self):
        return reverse(view_names.BLOG, kwargs={"slug": self.slug})
