"""Remove any 'dangling' objects from the database.

Currently, just removes tags which are no longer attached to anything."""
from django.core.management import BaseCommand
from main.tasks.cleanup import cleanup


class Command(BaseCommand):
    def handle(self, *args, **options):
        cleanup()
