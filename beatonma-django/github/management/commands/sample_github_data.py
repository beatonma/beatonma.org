import random
from typing import Optional

from django.core.management import BaseCommand
from django.utils import timezone
from github.models import (
    CachedResponse,
    GithubLanguage,
    GithubLicense,
    GithubRepository,
    GithubUser,
)

data = [
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
    {
        "id": "27999312691",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "45859f57a690a0843bf276ed46e3fe95c98db358",
                "url": "https://github.com/beatonma/whammy-arduino/commits/45859f57a690a0843bf276ed46e3fe95c98db358",
                "message": "Added missing resistors to switch GND connections.\n\nAlso minor layout fixes.",
            }
        ],
        "created_at": "2023-03-27 10:36:14+00:00",
        "repository": {
            "id": 483399730,
            "url": "https://github.com/beatonma/whammy-arduino",
            "name": "beatonma/whammy-arduino",
            "license": "gpl-3.0",
            "description": "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
        },
    },
    {
        "id": "27984992917",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "cb7508f038a4877b867b48c8444f2b69c778a7a3",
                "url": "https://github.com/beatonma/whammy-arduino/commits/cb7508f038a4877b867b48c8444f2b69c778a7a3",
                "message": "Update README.md\n\nAdded link to wiring diagram.",
            }
        ],
        "created_at": "2023-03-26 15:43:55+00:00",
        "repository": {
            "id": 483399730,
            "url": "https://github.com/beatonma/whammy-arduino",
            "name": "beatonma/whammy-arduino",
            "license": "gpl-3.0",
            "description": "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
        },
    },
    {
        "id": "27984944528",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "ad0a2ad2898746a14851a10a2ed27aa431932198",
                "url": "https://github.com/beatonma/whammy-arduino/commits/ad0a2ad2898746a14851a10a2ed27aa431932198",
                "message": "Added wiring diagram and updated config.h to match the same configuration.",
            }
        ],
        "created_at": "2023-03-26 15:37:28+00:00",
        "repository": {
            "id": 483399730,
            "url": "https://github.com/beatonma/whammy-arduino",
            "name": "beatonma/whammy-arduino",
            "license": "gpl-3.0",
            "description": "An Arduino-based MIDI controller for the Digitech Whammy IV effects pedal.",
        },
    },
    {
        "type": "PrivateEventSummary",
        "created_at": "2023-03-22 17:28:54+00:00",
        "event_count": 5,
        "repository_count": 1,
        "change_count": 12,
    },
    {
        "id": "27642348866",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "0f29f48550dadb26bbd5b6c2c921145923c40f35",
                "url": "https://github.com/beatonma/microformats-reader/commits/0f29f48550dadb26bbd5b6c2c921145923c40f35",
                "message": "h-feed updates",
            },
            {
                "sha": "823357af230c97e46498b83083ce74ae917ca461",
                "url": "https://github.com/beatonma/microformats-reader/commits/823357af230c97e46498b83083ce74ae917ca461",
                "message": "Filesystem restructure",
            },
            {
                "sha": "4888bb897c70f3739af2438e04d03a1b6dcc6404",
                "url": "https://github.com/beatonma/microformats-reader/commits/4888bb897c70f3739af2438e04d03a1b6dcc6404",
                "message": "Basic author component with expandable h-card.",
            },
            {
                "sha": "110c7e2cc82d38f4ffd8eb33f476db68400ad544",
                "url": "https://github.com/beatonma/microformats-reader/commits/110c7e2cc82d38f4ffd8eb33f476db68400ad544",
                "message": "Refactored scss.\n\nScss now collected via @use/@forward to single 'entrypoint': `app.scss`.\nThis is imported once in `popup.tsx`, creating a single global <style> in the final page.\n\nPreviously, importing files in the tsx module of use resulted in many <style> tags with a lot of duplication.",
            },
            {
                "sha": "8f8f3590411ae3a5251501db86d74ab74ecd60b9",
                "url": "https://github.com/beatonma/microformats-reader/commits/8f8f3590411ae3a5251501db86d74ab74ecd60b9",
                "message": "Styling refactor.\n\nRemoved unused css theming variables.\nReplaced --accent with --vibrant and --muted variants.\nImplemented injectTheme() - groundwork for potentially using source webpage colours or photos for theming.",
            },
            {
                "sha": "6baee7bb1f27a063ea00ae83070cde52e106ee7d",
                "url": "https://github.com/beatonma/microformats-reader/commits/6baee7bb1f27a063ea00ae83070cde52e106ee7d",
                "message": "Added Dialog element with scrim handling.",
            },
            {
                "sha": "82213fa1abd2d7134cce88a1c4128db89710ffc4",
                "url": "https://github.com/beatonma/microformats-reader/commits/82213fa1abd2d7134cce88a1c4128db89710ffc4",
                "message": "`nullable(obj, options)`: now accepts an options object.\n\noptions:\n requiredKeys: require all keys be present with non-empty values.\n requireAnyKey: require at least one key be present with non-empty value",
            },
            {
                "sha": "34ab39618097778452df2c4827cefdf168f446e3",
                "url": "https://github.com/beatonma/microformats-reader/commits/34ab39618097778452df2c4827cefdf168f446e3",
                "message": "Standardised border styling with %border-left and consistent use of --border-radius-x vars.",
            },
            {
                "sha": "3ebedac7d4978b5c32d76fd27c5f51eea25511fc",
                "url": "https://github.com/beatonma/microformats-reader/commits/3ebedac7d4978b5c32d76fd27c5f51eea25511fc",
                "message": "Removed <InlineGroup>, made obsolete by <Row> properties.\n\nAdded <Row> `spaced` property.\n- Applies column-gap with a standard value from RowSpace enum.\n- If defined with no explicit value, defaults to RowSpace.Normal -> `--space-1x` in css.",
            },
            {
                "sha": "20433dbbc2d6cc2cb9aa9b47585e43b610db3257",
                "url": "https://github.com/beatonma/microformats-reader/commits/20433dbbc2d6cc2cb9aa9b47585e43b610db3257",
                "message": "Added `initEntrypoint` to standardise page react element loading while setting document `title` and `lang` attributes.",
            },
            {
                "sha": "f2d71dc3a9bba5bf359d3dd17d71e7b9daa93c27",
                "url": "https://github.com/beatonma/microformats-reader/commits/f2d71dc3a9bba5bf359d3dd17d71e7b9daa93c27",
                "message": "Current git hash now available as `AppConfig.version`. Created options UI stub.",
            },
            {
                "sha": "0e04620a5e67717cab08f140a5e07b0fe6b6e0a1",
                "url": "https://github.com/beatonma/microformats-reader/commits/0e04620a5e67717cab08f140a5e07b0fe6b6e0a1",
                "message": "Added additional data from git.\n\n- Manifest version now derived from git commit count.\n- Added AppConfig fields `versionHash`, `versionDate`, `versionDescription`.",
            },
            {
                "sha": "8e00425e36115e1a9348bb2a52f86d0a9107db35",
                "url": "https://github.com/beatonma/microformats-reader/commits/8e00425e36115e1a9348bb2a52f86d0a9107db35",
                "message": "Refactored compat module, moved dev-patching of i18n to dev module.",
            },
            {
                "sha": "8338e86e61f73e34db360723e5d3939e51cc859e",
                "url": "https://github.com/beatonma/microformats-reader/commits/8338e86e61f73e34db360723e5d3939e51cc859e",
                "message": "Removed unused service worker",
            },
            {
                "sha": "533f0d746486a648fc14942e547c59a64e861e58",
                "url": "https://github.com/beatonma/microformats-reader/commits/533f0d746486a648fc14942e547c59a64e861e58",
                "message": "Renamed initEntrypoint -> initEntrypointUi",
            },
            {
                "sha": "0ade98247b3297d7c0c2b0b214859d6c20f16daf",
                "url": "https://github.com/beatonma/microformats-reader/commits/0ade98247b3297d7c0c2b0b214859d6c20f16daf",
                "message": "Implemented basic toolbar icon controls",
            },
            {
                "sha": "752283075970f63562048bb9fd51a796f7658d95",
                "url": "https://github.com/beatonma/microformats-reader/commits/752283075970f63562048bb9fd51a796f7658d95",
                "message": "Minor fixes",
            },
            {
                "sha": "8482caf0f559555de5a470195dd5ef828e96ddd3",
                "url": "https://github.com/beatonma/microformats-reader/commits/8482caf0f559555de5a470195dd5ef828e96ddd3",
                "message": "Moved parsing to content-script.ts so that the toolbar badge can be updated without needing to open the popup.",
            },
        ],
        "created_at": "2023-03-10 19:14:08+00:00",
        "repository": {
            "id": 86626264,
            "url": "https://github.com/beatonma/microformats-reader",
            "name": "beatonma/microformats-reader",
            "license": None,
            "description": "A browser extension that brings the Indieweb to the surface.",
        },
    },
    {
        "id": "27478467604",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "01af0b8b5d190cd8e7055d238342b54652c5d17f",
                "url": "https://github.com/beatonma/microformats-reader/commits/01af0b8b5d190cd8e7055d238342b54652c5d17f",
                "message": "Minor refactor",
            },
            {
                "sha": "64fe7effe0b76c079c4ec6eb96231621ee14b78c",
                "url": "https://github.com/beatonma/microformats-reader/commits/64fe7effe0b76c079c4ec6eb96231621ee14b78c",
                "message": "Refactored <Property>, <PropertyRow>.",
            },
            {
                "sha": "b205e966449903ce8bc96302176710bb4d0d19b0",
                "url": "https://github.com/beatonma/microformats-reader/commits/b205e966449903ce8bc96302176710bb4d0d19b0",
                "message": "Refactored <Property>, <PropertyRow>.",
            },
        ],
        "created_at": "2023-03-03 18:04:04+00:00",
        "repository": {
            "id": 86626264,
            "url": "https://github.com/beatonma/microformats-reader",
            "name": "beatonma/microformats-reader",
            "license": None,
            "description": "A browser extension that brings the Indieweb to the surface.",
        },
    },
    {
        "id": "27472690074",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "ee1a8558d141ec40841b6443b7246e0686f8fe52",
                "url": "https://github.com/beatonma/microformats-reader/commits/ee1a8558d141ec40841b6443b7246e0686f8fe52",
                "message": "Minor optimisation",
            },
            {
                "sha": "c5924269ae4847e071adaeb457f25e0d7bbfd619",
                "url": "https://github.com/beatonma/microformats-reader/commits/c5924269ae4847e071adaeb457f25e0d7bbfd619",
                "message": "Restructured parsing and display.\n\nParse functions are now strongly typed and simplified/deduplicated.\n\nParsed microformats now accept arrays for most fields instead of just taking the first value.\n - There are some exceptions to this, such as h-card images.\n\n<Property/>, <PropertyRow/> updated to display properties with multiple values.",
            },
            {
                "sha": "7742f9af6720555a318dad722ccaab1fbdcd33ea",
                "url": "https://github.com/beatonma/microformats-reader/commits/7742f9af6720555a318dad722ccaab1fbdcd33ea",
                "message": "Added OptionsContext for app configuration.",
            },
            {
                "sha": "5e04fff734f8bcc2b4031131aca894dfc5b0dad9",
                "url": "https://github.com/beatonma/microformats-reader/commits/5e04fff734f8bcc2b4031131aca894dfc5b0dad9",
                "message": "Restructured dev environment.\n\nNew entrypoint (`popup.dev.html` + `popup.dev.tsx`) for in-tab UI building.\n- Adds dev toolbar which allows choice of different sample HTML to use as data source.\n- Otherwise just wraps normal Popup UI.\n\nGlobal `AppConfig.isDebug` set by environment variable in `package.json` command.\n\nSome additional parsing logic to make sure empty components are not rendered.",
            },
            {
                "sha": "dbf8ca2a68831878ffb63fb6830419e243165b35",
                "url": "https://github.com/beatonma/microformats-reader/commits/dbf8ca2a68831878ffb63fb6830419e243165b35",
                "message": "Fallback to TextAvatar if photo fails to load.",
            },
            {
                "sha": "b7ee3306b2277efedf04008e63589ffa107dca1f",
                "url": "https://github.com/beatonma/microformats-reader/commits/b7ee3306b2277efedf04008e63589ffa107dca1f",
                "message": "Restructured dev environment.\n\nNew entrypoint (popup.dev.html + popup.dev.tsx) for in-tab UI building.\nAdds dev toolbar which allows choice of different sample HTML to use as data source.\n\nGlobal AppConfig.debug set by `package.json` `dev` command.",
            },
            {
                "sha": "1f88223c0e50908e2abef03f1713f6af80561aa7",
                "url": "https://github.com/beatonma/microformats-reader/commits/1f88223c0e50908e2abef03f1713f6af80561aa7",
                "message": "Show icon for organisation if jobTitle not available.",
            },
            {
                "sha": "7c3a7dbced615ef2f39db57d81e648e6f0c79d2b",
                "url": "https://github.com/beatonma/microformats-reader/commits/7c3a7dbced615ef2f39db57d81e648e6f0c79d2b",
                "message": "Fixed image parsing when `alt` not available.\nProperty can now accept an Image instead of an icon.",
            },
            {
                "sha": "8a8d2cb2109fe4ee87959a7a60f1d420d521d783",
                "url": "https://github.com/beatonma/microformats-reader/commits/8a8d2cb2109fe4ee87959a7a60f1d420d521d783",
                "message": "Extracted ExpandableCard component from HCard for reuse.",
            },
            {
                "sha": "61c5b695d7e353d9de5aa1c794344ab58599b201",
                "url": "https://github.com/beatonma/microformats-reader/commits/61c5b695d7e353d9de5aa1c794344ab58599b201",
                "message": "ExpandCollapseLayout/Dropdown can no longer change state when it has no child nodes",
            },
            {
                "sha": "38144c756fad03081afcdcc0f0a466fb89bd2269",
                "url": "https://github.com/beatonma/microformats-reader/commits/38144c756fad03081afcdcc0f0a466fb89bd2269",
                "message": "Refactor",
            },
            {
                "sha": "fd3b982759ad106f270944ce98a6ab55083028d9",
                "url": "https://github.com/beatonma/microformats-reader/commits/fd3b982759ad106f270944ce98a6ab55083028d9",
                "message": "Improved mocking of i18n.getMessage when running in test/dev environment.\n\nNow handles placeholder args correctly.",
            },
            {
                "sha": "9057200fd328708ce6b418fb6279eb4930e952d6",
                "url": "https://github.com/beatonma/microformats-reader/commits/9057200fd328708ce6b418fb6279eb4930e952d6",
                "message": "Improved datetime formatting",
            },
            {
                "sha": "1087f07debbdbb79fffb316f957b641e7a41d543",
                "url": "https://github.com/beatonma/microformats-reader/commits/1087f07debbdbb79fffb316f957b641e7a41d543",
                "message": "Moved `takeIfNotEmpty`",
            },
            {
                "sha": "f13888f18b20f1fcee473b910b0644f980834f08",
                "url": "https://github.com/beatonma/microformats-reader/commits/f13888f18b20f1fcee473b910b0644f980834f08",
                "message": "Improved datetime formatting",
            },
            {
                "sha": "735404340faceb38b3b4835cb7ea755a0343609b",
                "url": "https://github.com/beatonma/microformats-reader/commits/735404340faceb38b3b4835cb7ea755a0343609b",
                "message": "`dt` elements are now parsed as Date objects immediately (previously deferred handling to UI elements).\n\n<Property> `displayValue` now accepts Date objects.",
            },
            {
                "sha": "469b7026a4031020235ba93fabcca0a8295a1cf3",
                "url": "https://github.com/beatonma/microformats-reader/commits/469b7026a4031020235ba93fabcca0a8295a1cf3",
                "message": "Added tests for array and object util functions.\n\nnullable(obj) now accepts an optional list of keys that should be ignored\n- i.e. the result can be null even if those keys have non-null values.",
            },
            {
                "sha": "098885d0409895fd6b9d4e4b9930998409123e65",
                "url": "https://github.com/beatonma/microformats-reader/commits/098885d0409895fd6b9d4e4b9930998409123e65",
                "message": "Introduced EmbeddedHCard interface.\n\nThis is the result of parsing a property that may be either a simple 'name' string, or a complex embedded hcard.",
            },
        ],
        "created_at": "2023-03-03 13:58:20+00:00",
        "repository": {
            "id": 86626264,
            "url": "https://github.com/beatonma/microformats-reader",
            "name": "beatonma/microformats-reader",
            "license": None,
            "description": "A browser extension that brings the Indieweb to the surface.",
        },
    },
    {
        "type": "PrivateEventSummary",
        "created_at": "2023-02-20 19:55:53+00:00",
        "event_count": 4,
        "repository_count": 3,
        "change_count": 7,
    },
    {
        "id": "27025681363",
        "type": "PushEvent",
        "payload": [
            {
                "sha": "2f7834b346e70fddaebc361fcbb06360a5702636",
                "url": "https://github.com/beatonma/microformats-reader/commits/2f7834b346e70fddaebc361fcbb06360a5702636",
                "message": "Parsers are now async.",
            },
            {
                "sha": "b9c5b39550ff727cb534d136ccc7cad02cb68797",
                "url": "https://github.com/beatonma/microformats-reader/commits/b9c5b39550ff727cb534d136ccc7cad02cb68797",
                "message": "Deleted unused files from original release.",
            },
            {
                "sha": "254a486f3b28309106d31e4bc744237444264aa8",
                "url": "https://github.com/beatonma/microformats-reader/commits/254a486f3b28309106d31e4bc744237444264aa8",
                "message": "Updated tests for async parser.",
            },
            {
                "sha": "f1f46d70a5ab026c1f5abb43e6815138a3035b86",
                "url": "https://github.com/beatonma/microformats-reader/commits/f1f46d70a5ab026c1f5abb43e6815138a3035b86",
                "message": "Refactored for reusable CardLayout",
            },
            {
                "sha": "c811009585c11193461c2dfa1d84c8c6fec77f56",
                "url": "https://github.com/beatonma/microformats-reader/commits/c811009585c11193461c2dfa1d84c8c6fec77f56",
                "message": "Refactored for reusable CardLayout",
            },
            {
                "sha": "044054fc0f8b3934dbf725927d504ae2802222d9",
                "url": "https://github.com/beatonma/microformats-reader/commits/044054fc0f8b3934dbf725927d504ae2802222d9",
                "message": "Test refactoring",
            },
            {
                "sha": "11040ab5533640295065e4fa4d23047e6144dcc0",
                "url": "https://github.com/beatonma/microformats-reader/commits/11040ab5533640295065e4fa4d23047e6144dcc0",
                "message": "Checkpoint: Basic h-feed parse and rendering.",
            },
            {
                "sha": "cc575ab57e27ddc0e2f25fb542d18ae5e9bffe84",
                "url": "https://github.com/beatonma/microformats-reader/commits/cc575ab57e27ddc0e2f25fb542d18ae5e9bffe84",
                "message": "Reinstated missing link to maps.",
            },
            {
                "sha": "e5751548131c94509305666c95a2f912252d5fbd",
                "url": "https://github.com/beatonma/microformats-reader/commits/e5751548131c94509305666c95a2f912252d5fbd",
                "message": "Enabled typescript strict mode.",
            },
            {
                "sha": "15faa9e6620124ca31699dcc358ad8dd9a36bddc",
                "url": "https://github.com/beatonma/microformats-reader/commits/15faa9e6620124ca31699dcc358ad8dd9a36bddc",
                "message": "Split monolithic Microformats enum into more specific enums within Microformat namespace.\n\nThis allows us to have a function that only accepts `h-` property names, for example.\ne.g. Parse.getRootsOfType()",
            },
            {
                "sha": "0e0d8bb0c789e7dc542c78741c54364282a197b7",
                "url": "https://github.com/beatonma/microformats-reader/commits/0e0d8bb0c789e7dc542c78741c54364282a197b7",
                "message": "Added category and content",
            },
        ],
        "created_at": "2023-02-11 15:19:30+00:00",
        "repository": {
            "id": 86626264,
            "url": "https://github.com/beatonma/microformats-reader",
            "name": "beatonma/microformats-reader",
            "license": None,
            "description": "A browser extension that brings the Indieweb to the surface.",
        },
    },
    {
        "type": "PrivateEventSummary",
        "created_at": "2023-01-31 20:42:50+00:00",
        "event_count": 38,
        "repository_count": 2,
        "change_count": 73,
    },
    {
        "id": "26217039054",
        "type": "IssuesEvent",
        "payload": {
            "url": "https://github.com/beatonma/django-wm/issues/45",
            "number": 45,
            "closed_at": "2023-01-04 11:52:59+00:00",
        },
        "created_at": "2023-01-04 11:53:00+00:00",
        "repository": {
            "id": 179150364,
            "url": "https://github.com/beatonma/django-wm",
            "name": "beatonma/django-wm",
            "license": "gpl-3.0",
            "description": "Automatic Webmention functionality for Django models",
        },
    },
]


LANGUAGES = [
    "Kotlin",
    "Python",
    "Typescript",
]


_sample_repo_id = 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        CachedResponse.objects.get_or_create(data=data)

        _create_repositories()


def _create_repositories():
    public_repo = create_repository(
        name="Github project repo",
        description="A sample github repository",
        is_public=True,
    )
    private_repo = create_repository(
        name="PRIVATE_REPOSITORY",
        description="THIS SHOULD NEVER BE PUBLICLY VISIBLE",
        is_public=False,
    )

    public_repo.tags.add("sample-tag")
    private_repo.tags.add("sample-tag")


def create_repository(
    name: str = None,
    description: str = None,
    is_public: bool = True,
):
    global _sample_repo_id

    try:
        repo = GithubRepository.objects.get(id=_sample_repo_id)
    except GithubRepository.DoesNotExist:
        repo = GithubRepository.objects.create(
            id=_sample_repo_id,
            url="https://fake-github.com/beatonma/my-repo",
            updated_at=timezone.now(),
            name=name,
            full_name=name,
            description=description,
            size_kb=random.randint(1, 20480),
            is_private=not is_public,
            is_published=is_public,
            primary_language=create_language(),
            license=generate_license(),
            owner=generate_user(),
        )

    _sample_repo_id += 1
    return repo


def create_language(name: Optional[str] = None):
    lang, _ = GithubLanguage.objects.get_or_create(
        name=name or random.choice(LANGUAGES)
    )

    return lang


def generate_license():
    _license, _ = GithubLicense.objects.get_or_create(
        key="mit",
        defaults={"name": "MIT License", "url": "https://api.github.com/licenses/mit"},
    )
    return _license


def generate_user():
    user, _ = GithubUser.objects.get_or_create(
        id=1,
        defaults={
            "username": "beatonma",
            "url": "https://fake-github.com/beatonma/",
            "avatar_url": "https://i.pravatar.cc/64",
        },
    )
    return user
