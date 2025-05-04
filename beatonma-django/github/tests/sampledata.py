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
    global _sample_repo_id
    _sample_repo_id += 1
    return _sample_repo_id


def create_sample_repository(
    name: str,
    is_private: bool,
    is_published: bool,
    description: str = None,
):
    repo, _ = GithubRepository.objects.get_or_create(
        name=name,
        defaults={
            "id": __sample_repo_id(),  # Field is retrieved from API, not auto-incremented.
            "url": "https://fake-github.com/beatonma/my-repo",
            "full_name": name,
            "description": description,
            "is_private": is_private,
            "is_published": is_published,
            "updated_at": timezone.now(),
            "size_kb": random.randint(1, 20480),
            "primary_language": create_sample_language(),
            "license": generate_sample_license(),
            "owner": generate_sample_user(),
        },
    )

    return repo


def create_sample_language(name: str = None):
    lang, _ = GithubLanguage.objects.get_or_create(
        name=name or random.choice(LANGUAGES)
    )

    return lang


def generate_sample_license():
    _license, _ = GithubLicense.objects.get_or_create(
        key="mit",
        defaults={"name": "MIT License", "url": "https://api.github.com/licenses/mit"},
    )
    return _license


def generate_sample_user():
    user, _ = GithubUser.objects.get_or_create(
        id=1,
        defaults={
            "username": "beatonma",
            "url": "https://fake-github.com/beatonma/",
            "avatar_url": "https://i.pravatar.cc/64",
        },
    )
    return user
