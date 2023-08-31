import logging
from datetime import date

from common.models import BaseModel
from common.models.util import implementations_of
from django.core.management import BaseCommand
from main.tests.create_test_data import create_test_data

log = logging.getLogger(__name__)


TESTDATA_DATE = date(2023, 2, 3)


class Command(BaseCommand):
    """Create sample data for running frontend tests."""

    models = implementations_of(BaseModel)

    def handle(self, *args, **options):
        self.clear()

        create_test_data()

    def clear(self):
        for Model in self.models:
            Model.objects.all().delete()
