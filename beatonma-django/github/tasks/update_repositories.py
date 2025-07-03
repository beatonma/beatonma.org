from datetime import datetime

from celery.utils.log import get_task_logger
from common.util import http
from github import github_api
from github.models import (
    GithubLanguage,
    GithubLanguageUsage,
    GithubLicense,
    GithubRepository,
    GithubUser,
)
from ninja import Schema
from pydantic import Field

log = get_task_logger(__name__)


def update_github_repository_cache():
    url = "https://api.github.com/user/repos"
    params = {
        "sort": "updated",
    }

    github_api.for_each(
        url,
        _update_repository,
        params=params,
    )


class GithubUserData(Schema):
    username: str = Field(validation_alias="login")
    id: int
    profile_url: str = Field(validation_alias="html_url")
    avatar_url: str


class GithubLicenseData(Schema):
    key: str
    name: str
    url: str


class GithubRepoData(Schema):
    id: int
    name: str
    full_name: str
    description: str | None
    html_url: str
    is_private: bool = Field(validation_alias="private")
    size_kb: int = Field(validation_alias="size")
    created_at: datetime
    updated_at: datetime
    topics: list[str]
    license: GithubLicenseData | None
    owner: GithubUserData
    primary_language: str | None = Field(validation_alias="language")


def _update_repository(obj: dict):
    """See: https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user"""

    data: GithubRepoData = GithubRepoData.model_validate(obj)
    _license = _update_license(data.license)
    owner = _update_owner(data.owner)
    primary_language = _get_language(data.primary_language)

    repo: GithubRepository
    created: bool
    repo, created = GithubRepository.objects.update_or_create(
        id=data.id,
        defaults={
            "owner": owner,
            "license": _license,
            "url": data.html_url,
            "is_private": data.is_private,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "published_at": data.created_at,
            "name": data.name,
            "full_name": data.full_name,
            "description": data.description,
            "size_kb": data.size_kb,
            "primary_language": primary_language,
        },
    )

    if created:
        repo.is_published = not data.is_private
        repo.save(update_fields=["is_published"])

    repo.tags.add(*data.topics)

    _update_languages(repo)


def _update_languages(repo: GithubRepository):
    username = repo.owner.username

    url = f"https://api.github.com/repos/{username}/{repo.name}/languages"

    try:
        response = github_api.get_if_changed(url)
        if response.status_code == http.STATUS_304_NOT_MODIFIED:
            return

    except github_api.GithubApiException as e:
        log.warning(e)
        return

    data: dict[str, int] = response.json()
    for language_name, byte_count in data.items():
        language = _get_language(language_name)

        GithubLanguageUsage.objects.update_or_create(
            language=language,
            repository=repo,
            defaults={
                "size_bytes": byte_count,
            },
        )


def _update_owner(data: GithubUserData) -> GithubUser:
    owner, _ = GithubUser.objects.update_or_create(
        id=data.id,
        defaults={
            "username": data.username,
            "url": data.profile_url,
            "avatar_url": data.avatar_url,
        },
    )
    return owner


def _update_license(data: GithubLicenseData | None) -> GithubLicense | None:
    if data is None:
        return None

    _license, _ = GithubLicense.objects.update_or_create(
        key=data.key,
        defaults={
            "name": data.name,
            "url": data.url,
        },
    )

    return _license


def _get_language(name: str | None) -> GithubLanguage | None:
    if name:
        language, _ = GithubLanguage.objects.get_or_create(name=name)
        return language
