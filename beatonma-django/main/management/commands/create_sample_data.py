import logging

from django.core.management import BaseCommand
from github.models import CachedResponse
from main.models import AboutPost, AppPost, ChangelogPost, Post
from main.tasks.sample_data import generate_posts
from taggit.models import Tag

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """Generate sample data for frontend development."""

    models = [
        AboutPost,
        AppPost,
        ChangelogPost,
        Post,
        Tag,
        CachedResponse,
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            default=False,
        )

    def handle(self, *args, clear: bool, **options):
        if clear:
            self.clear()

        if self.is_empty():
            log.info("Generating new sample data")
            generate_posts()
        else:
            log.info("Sample data already populated")

    def is_empty(self) -> bool:
        for Model in self.models:
            if Model.objects.all().exists():
                return False
        return True

    def clear(self):
        for Model in self.models:
            Model.objects.all().delete()
