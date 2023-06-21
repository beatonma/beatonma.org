from common.management.async_command import AsyncCommand
from github.tasks import update_github_repos_and_events


class Command(AsyncCommand):
    def handle(self, *args, **options):
        self.handle_async(update_github_repos_and_events, **options)
