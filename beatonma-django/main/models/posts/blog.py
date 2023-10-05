from django.urls import reverse
from main.models.mixins.themeable import ThemeableMixin
from main.models.posts.webpost import RichWebPost
from main.view_adapters import FeedItemContext
from main.views import view_names


class Blog(ThemeableMixin, RichWebPost):
    """An informal post."""

    def get_absolute_url(self):
        return reverse(view_names.BLOG, kwargs={"slug": self.slug})

    def to_feeditem_context(self) -> FeedItemContext:
        try:
            image_url = self.file_url_list()[0]
        except IndexError:
            image_url = None

        return FeedItemContext(
            title=self.title,
            url=self.get_absolute_url(),
            date=self.published_at,
            type=self.__class__.__name__,
            summary=self.preview_text,
            image_url=image_url,
            image_class="cover",
            themeable=self,
        )
