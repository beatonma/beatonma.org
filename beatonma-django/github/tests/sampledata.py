import random
from typing import Optional

from django.utils import timezone
from github.models import GithubLanguage, GithubLicense, GithubRepository, GithubUser

LANGUAGES = [
    "Kotlin",
    "Python",
    "Typescript",
]

_sample_repo_id: int = 1


def create_sample_repository(
    name: str,
    is_private: bool,
    is_published: bool,
    description: str = None,
):
    global _sample_repo_id
    repo = GithubRepository.objects.create(
        id=_sample_repo_id,
        url="https://fake-github.com/beatonma/my-repo",
        updated_at=timezone.now(),
        name=name,
        full_name=name,
        description=description,
        size_kb=random.randint(1, 20480),
        is_private=is_private,
        is_published=is_published,
        primary_language=create_sample_language(),
        license=generate_sample_license(),
        owner=generate_sample_user(),
    )
    _sample_repo_id += 1

    return repo


def create_sample_language(name: Optional[str] = None):
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
