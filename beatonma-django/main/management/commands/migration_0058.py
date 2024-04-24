from django.core.management import BaseCommand
from main.models import RelatedFile


class Command(BaseCommand):
    def handle(self, *args, **options):
        related_files = RelatedFile.objects.all()

        # Trigger save() to update new `type` field.
        for related_file in related_files:
            related_file.save()
