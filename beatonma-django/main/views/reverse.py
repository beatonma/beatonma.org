from typing import Union

from django.urls import reverse
from github.models import GithubLanguage
from main.views import view_names
from taggit.models import Tag


def language(lang: GithubLanguage) -> str:
    return reverse(view_names.LANGUAGES, args=[lang.name])


def tag(tag_: Union[Tag, str]) -> str:
    tagname = tag_ if isinstance(tag_, str) else tag_.name

    return reverse(view_names.TAGS, args=[tagname])
