import logging
from datetime import date

from common.models import BaseModel
from common.models.util import implementations_of
from django.core.management import BaseCommand
from github.management.commands.sample_github_data import create_repository
from github.models import CachedResponse
from main.tasks import sample_data as sample
from main.tasks.sample_data import HCardConfig, create_about_page

log = logging.getLogger(__name__)


TESTDATA_DATA = date(2023, 2, 3)


class Command(BaseCommand):
    """Create sample data for running frontend tests."""

    models = implementations_of(BaseModel)

    def handle(self, *args, **options):
        self.clear()

        for n in range(30):
            # Force pagination
            sample.create_note()

        self.generate(published=True)
        self.generate(published=False)

        CachedResponse.objects.get_or_create(
            data=[
                {
                    "id": "27999829329",
                    "type": "PushEvent",
                    "payload": [
                        {
                            "sha": "0cee90da75c45e9001f2e03a71e1ee2cc0b2e611",
                            "url": "https://github.com/beatonma/whammy-arduino/commits/0cee90da75c45e9001f2e03a71e1ee2cc0b2e611",
                            "message": "Minor layout tweaks. Added png render in case of differences with fonts or whatever.",
                        }
                    ],
                    "created_at": "2023-03-27 10:58:04+00:00",
                    "repository": {
                        "id": 483399730,
                        "url": "https://github.com/beatonma/whammy-arduino",
                        "name": "beatonma/whammy-arduino",
                        "license": "gpl-3.0",
                        "description": "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
                    },
                },
            ]
        )

    def generate(self, published: bool):
        tags = ["sample-tag"]

        label = "TestTarget" if published else "__PRIVATE__"

        about = create_about_page(
            description="target",
            content="TestTarget about content",
        )
        language = sample.create_language(name="TestTarget-Language")
        app_type = sample.create_app_type(
            name="TestTarget-AppType",
            date=TESTDATA_DATA,
        )

        article = sample.create_article(
            title=f"{label} Article",
            preview_text=f"{label} Article preview",
            is_published=published,
            tags=tags,
            date=TESTDATA_DATA,
        )
        blog = sample.create_blog(
            title=f"{label} Blog",
            preview_text=f"{label} Blog preview",
            is_published=published,
            tags=tags,
            date=TESTDATA_DATA,
        )
        note = sample.create_note(
            content=f"{label} Note",
            is_published=published,
            tags=tags,
            date=TESTDATA_DATA,
        )
        app = sample.create_app(
            title=f"{label} App",
            app_type=app_type,
            is_published=published,
            tags=tags,
            language=language.name,
            date=TESTDATA_DATA,
        )
        changelog = sample.create_changelog(
            app,
            content=f"{label} changelog content",
            version_name=f"1.0-{label}",
            preview_text="Target changelog preview",
            is_published=published,
            tags=tags,
            date=TESTDATA_DATA,
        )
        repo = create_repository(
            name=f"{label} Repo",
            description=f"{label} repo description",
            is_public=published,
        )

        sample.create_hcard(
            HCardConfig(
                "TestTarget Name",
                "https://target-url.org",
                "https://target-url.org/avatar",
            )
        )
        sample.generate_webmentions(force_hcard=True)

    def clear(self):
        for Model in self.models:
            Model.objects.all().delete()
