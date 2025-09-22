import random

from django.utils import timezone
from github.models import GithubLanguage, GithubLicense, GithubRepository, GithubUser

LANGUAGES = [
    "Kotlin",
    "Python",
    "Typescript",
]

_sample_repo_id: int = 1


def __sample_repo_id() -> int:
    # id field is retrieved from API, not auto-incremented.
    global _sample_repo_id
    _sample_repo_id += 1
    return _sample_repo_id


def get_sample_repository(
    name: str,
    is_private: bool,
    is_published: bool | None = None,
    id: int | None = None,
    description: str = None,
    owner: GithubUser | None = None,
):
    repo, _ = GithubRepository.objects.get_or_create(
        name=name,
        defaults={
            "id": id or __sample_repo_id(),
            "url": "https://fake-github.com/beatonma/my-repo",
            "full_name": name,
            "description": description,
            "is_private": is_private,
            "is_published": not is_private if is_published is None else is_published,
            "updated_at": timezone.now(),
            "size_kb": random.randint(1, 20480),
            "primary_language": get_sample_language(),
            "license": get_sample_license(),
            "owner": owner or get_sample_user(),
        },
    )

    return repo


def get_sample_language(name: str = None):
    lang, _ = GithubLanguage.objects.get_or_create(
        name=name or random.choice(LANGUAGES)
    )

    return lang


def get_sample_license():
    _license, _ = GithubLicense.objects.get_or_create(
        key="mit",
        defaults={"name": "MIT License", "url": "https://api.github.com/licenses/mit"},
    )
    return _license


def get_sample_user():
    user, _ = GithubUser.objects.get_or_create(
        id=12682046,
        defaults={
            "username": "beatonma",
            "url": "https://fake-github.com/beatonma/",
            "avatar_url": "https://i.pravatar.cc/64",
        },
    )
    return user
