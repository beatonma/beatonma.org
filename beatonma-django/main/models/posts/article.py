from django.db import models
from django.urls import reverse
from main.forms import SanitizedFileField
from main.models.formats import Formats
from main.models.mixins.themeable import ThemeableMixin
from main.models.posts.webpost import RichWebPost
from main.view_adapters import FeedItemContext
from main.views import view_names


class Article(ThemeableMixin, RichWebPost):
    """A somewhat formal write-up about a thing."""

    IMAGE_FIT_OPTIONS = (
        ("contain", "contain"),
        ("cover", "cover"),
    )

    abstract = models.CharField(max_length=1024, blank=True, help_text="tl;dr")
    abstract_html = models.TextField(blank=True)

    content_script = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Any post-specific scripts or styles that need to "
            "be added at the end of the <body> HTML tag."
        ),
    )

    apps = models.ManyToManyField(
        "main.App",
        blank=True,
        related_name="article",
        help_text="Choose any apps that this article talks about",
    )

    preview_image = SanitizedFileField(
        blank=True,
        upload_to="article/%Y/",
        filename_literals=["preview"],
        size=[800, 800],
        help_text="Image shown beside links to this article",
    )
    hero_image = SanitizedFileField(
        blank=True,
        upload_to="article/%Y/",
        filename_literals=["hero"],
        help_text="Image shown at the top of the article",
    )
    hero_html = models.TextField(
        blank=True,
        help_text="Replace the hero image area with something else",
    )

    preview_image_css = models.CharField(
        max_length=80,
        blank=True,
        choices=IMAGE_FIT_OPTIONS,
        default="cover",
        help_text="CSS class",
    )
    hero_css = models.CharField(
        max_length=80,
        blank=True,
        choices=IMAGE_FIT_OPTIONS,
        default="cover",
        help_text="CSS class",
    )
    hero_banner_css = models.CharField(
        max_length=80,
        blank=True,
        choices=IMAGE_FIT_OPTIONS,
        default="contain",
        help_text="contain: border around image. cover: full-width primary color",
    )

    def get_absolute_url(self):
        return reverse(view_names.ARTICLE, kwargs={"slug": self.slug})

    def get_content_html(self):
        return f"{self.title} {self.abstract_html} {self.content_html}"

    def save_text(self):
        super().save_text()
        self.abstract_html = Formats.to_html(self.format, self.abstract)

    def to_feeditem_context(self) -> FeedItemContext:
        try:
            image_url = self.preview_image.url
        except ValueError:
            image_url = None

        return FeedItemContext(
            title=self.title,
            url=self.get_absolute_url(),
            date=self.published_at,
            type=self.__class__.__name__,
            summary=self.preview_text,
            image_url=image_url,
            image_class=self.preview_image_css,
            themeable=self,
        )
