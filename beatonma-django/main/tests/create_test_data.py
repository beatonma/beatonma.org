from datetime import date

from github.management.commands import sample_github_data as sample_github
from github.models import CachedResponse
from main.tasks import sample_data as sample

TESTDATA_DATE = date(2023, 2, 3)


def create_test_data():
    for n in range(30):
        # Force pagination
        sample.create_note()

    _generate(published=True)
    _generate(published=False)

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


def _generate(published: bool):
    tags = ["sample-tag"]

    label = "TestTarget" if published else "__PRIVATE__ TestTarget"

    about = sample.create_about_page(
        description="target",
        content="TestTarget about content",
    )
    motd = sample.create_motd(
        f"{label} MOTD",
        f"{label} MOTD content",
        is_published=published,
    )
    language = sample.create_language(name="TestTarget-Language")
    app_type = sample.create_app_type(
        name="TestTarget-AppType",
        date=TESTDATA_DATE,
    )

    article = sample.create_article(
        title=f"{label} Article",
        preview_text=f"{label} Article preview",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
    )
    blog = sample.create_blog(
        title=f"{label} Blog",
        preview_text=f"{label} Blog preview",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
    )
    note = sample.create_note(
        content=f"{label} Note",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
    )
    app = sample.create_app(
        title=f"{label} App",
        app_type=app_type,
        is_published=published,
        tags=tags,
        language=language.name,
        date=TESTDATA_DATE,
    )
    changelog = sample.create_changelog(
        app,
        content=f"{label} changelog content",
        version_name=f"1.0-{label}",
        preview_text="Target changelog preview",
        is_published=published,
        tags=tags,
        date=TESTDATA_DATE,
    )
    repo = sample_github.create_repository(
        name=f"{label} Repo",
        description=f"{label} repo description",
        is_public=published,
    )

    sample.create_hcard(
        sample.HCardConfig(
            "TestTarget Name",
            "https://target-url.org",
            "https://target-url.org/avatar",
        )
    )
    sample.generate_webmentions(force_hcard=True)
