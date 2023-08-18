from django.core.management import BaseCommand
from github.tasks import prebuild_cached_response


class Command(BaseCommand):
    """Without refreshing the source data from Github,
    reconstruct the cached  response for GithubEventsView."""

    def handle(self, *args, **options):
        prebuild_cached_response()
