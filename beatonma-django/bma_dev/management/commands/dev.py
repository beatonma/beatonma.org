from django.core.management import BaseCommand


class Command(BaseCommand):
    """Placeholder management command which can be implemented as needed."""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        raise Exception("Dev task is not currently implemented")
