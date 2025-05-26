import logging
from datetime import date

from common.models import BaseModel
from common.models.util import implementations_of
from django.core.management import BaseCommand
from github.management.commands import sample_github_data as sample_github
from github.models import CachedResponse
from main.models import SiteHCard
from main.tasks import sample_data as sample

log = logging.getLogger(__name__)


TESTDATA_DATE = date.today()


class Command(BaseCommand):
    """Create data with specific values for running frontend tests."""

    models = implementations_of(BaseModel)

    def handle(self, *args, **options):
        self.clear()

        _create_test_data()

    def clear(self):
        for Model in self.models:
            Model.objects.all().delete()


def _create_test_data():
    for n in range(30):
        # Force pagination
        sample.create_post()

    _generate_publishable(published=True)
    _generate_publishable(published=False)

    _generate_about()
    _generate_microformat_content()
    _generate_github()


def _generate_about():
    about_root = sample.create_about_page(
        title="target",
        content="<!-- h-card -->\n\nTestTarget about content with hcard",
    )
    sample.create_about_page(
        parent=about_root, title="Leaf", content="about something specific"
    )


def _generate_github():
    CachedResponse.objects.get_or_create(
        data={
            "events": [
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
        }
    )


def _generate_publishable(published: bool):
    tags = ["sample-tag"]

    label = "TestTarget" if published else "__PRIVATE__ TestTarget"

    def _slug(slug: str):
        return slug if published else f"__PRIVATE__{slug}"

    sample.create_motd(
        f"{label} MOTD",
        f"{label} MOTD content",
        is_published=published,
    )

    sample.create_post(
        title=f"{label} Article",
        preview=f"{label} Article preview",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
        slug=_slug("test-article"),
    )
    sample.create_post(
        title=f"{label} Blog",
        preview=f"{label} Blog preview",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
        slug=_slug("test-blog"),
    )
    sample.create_post(
        content=f"{label} Note",
        preview=f"{label} Note",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
        slug=_slug("test-note"),
    )
    app = sample.create_app(
        title=f"{label} App",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
        slug=_slug("test-app"),
    )
    sample.create_changelog(
        app,
        content=f"{label} changelog content",
        version=f"1.0-{label}",
        preview="Target changelog preview",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
        slug=_slug("test-changelog"),
    )
    sample_github.create_sample_repository(
        name=f"{label} Repo",
        description=f"{label} repo description",
        is_published=published,
        is_private=not published,
    )


def _generate_microformat_content():
    SiteHCard.objects.create(
        name="Firstname Surname",
    )

    sample.create_hcard(
        sample.HCardConfig(
            "TestTarget Name",
            "https://target-url.org",
            "https://target-url.org/avatar",
        )
    )
    sample.generate_webmentions(force_hcard=True)
