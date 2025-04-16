from bma_dev.tools import Timer
from django.core.management import BaseCommand
from main.api.querysets import get_feed


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("n", nargs="?", default=10, type=int)

        parser.add_argument("--query")
        parser.add_argument("--tag")

    def handle(self, *args, n, query=None, tag=None, **options):
        timer = Timer(print_result=False)
        with timer:
            for _ in range(n):
                with timer.sub():
                    list(get_feed(query=query, tag=tag))

        print(timer.report())
