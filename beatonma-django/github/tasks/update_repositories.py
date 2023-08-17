from datetime import datetime
from typing import Dict, List, Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from github import github_api
from github.models import (
    GithubLanguage,
    GithubLanguageUsage,
    GithubLicense,
    GithubRepository,
    GithubUser,
)
from github.tasks.util import parse_datetime

log = get_task_logger(__name__)


@shared_task
def update_github_repository_cache():
    url = "https://api.github.com/user/repos"
    params = dict(
        sort="updated",
    )

    github_api.for_each(
        url,
        _update_repository,
        params=params,
    )


class ApiData:
    pass


class GithubUserData(ApiData):
    username: str
    id: int
    profile_url: str
    avatar_url: str

    def __init__(self, login: str, id: int, html_url: str, avatar_url: str, **kwargs):
        self.username = login
        self.id = id
        self.profile_url = html_url
        self.avatar_url = avatar_url


class GithubLicenseData(ApiData):
    key: str
    name: str
    url: str

    def __init__(self, key: str, name: str, url: str, **kwargs):
        self.key = key
        self.name = name
        self.url = url


class GithubRepoData(ApiData):
    id: int
    name: str
    full_name: str
    description: str
    html_url: str
    private: bool
    size_kb: int
    created_at: datetime
    updated_at: datetime
    topics: List[str]

    def __init__(
        self,
        id: int,
        name: str,
        full_name: str,
        description: str,
        html_url: str,
        private: bool,
        size: int,
        created_at: str,
        updated_at: str,
        topics: List[str],
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.description = description
        self.html_url = html_url
        self.private = private
        self.size_kb = size
        self.created_at = parse_datetime(created_at)
        self.updated_at = parse_datetime(updated_at)
        self.topics = topics


def _update_repository(obj: dict):
    """See: https://docs.github.com/en/rest/reference/repos#list-repositories-for-the-authenticated-user"""

    owner = _update_owner(obj["owner"])
    _license = _update_license(obj["license"])
    primary_language = _get_language(obj["language"])

    data = GithubRepoData(**obj)

    repo: GithubRepository
    created: bool
    repo, created = GithubRepository.objects.update_or_create(
        id=data.id,
        defaults=dict(
            owner=owner,
            license=_license,
            url=data.html_url,
            is_private=data.private,
            created_at=data.created_at,
            updated_at=data.updated_at,
            published_at=data.created_at,
            name=data.name,
            full_name=data.full_name,
            description=data.description,
            size_kb=data.size_kb,
            primary_language=primary_language,
        ),
    )

    if created:
        repo.is_published = not data.private
        repo.save(update_fields=["is_published"])

    repo.tags.add(*data.topics)

    _update_languages(repo)


def _update_languages(repo: GithubRepository):
    username = repo.owner.username

    url = f"https://api.github.com/repos/{username}/{repo.name}/languages"

    try:
        response = github_api.get_if_changed(url)
        if response is None:
            return

    except github_api.GithubApiException as e:
        log.warning(e)
        return

    data: Dict[str, int] = response.json()
    for language_name, byte_count in data.items():
        language = _get_language(language_name)

        GithubLanguageUsage.objects.update_or_create(
            language=language,
            repository=repo,
            defaults=dict(
                size_bytes=byte_count,
            ),
        )


def _update_owner(obj: dict) -> GithubUser:
    data = GithubUserData(**obj)

    owner, _ = GithubUser.objects.update_or_create(
        id=data.id,
        defaults=dict(
            username=data.username,
            url=data.profile_url,
            avatar_url=data.avatar_url,
        ),
    )
    return owner


def _update_license(obj: dict) -> Optional[GithubLicense]:
    if obj is None:
        return None

    data = GithubLicenseData(**obj)

    _license, _ = GithubLicense.objects.update_or_create(
        key=data.key,
        defaults=dict(
            name=data.name,
            url=data.url,
        ),
    )

    return _license


def _get_language(name: Optional[str]) -> Optional[GithubLanguage]:
    if name:
        language, _ = GithubLanguage.objects.get_or_create(name=name)
        return language
