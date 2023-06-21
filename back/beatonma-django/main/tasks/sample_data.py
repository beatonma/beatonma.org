import random
from collections import namedtuple
from datetime import date as Date
from datetime import datetime, timezone
from typing import List, Optional, Union
from urllib.parse import urljoin

from common.models import TaggableMixin
from common.models.util import implementations_of
from django.db.models import QuerySet
from django.utils.text import slugify
from github.management.commands.sample_github_data import create_language
from main.models import App, AppType, Article, Blog, Changelog, Note
from main.models.posts import About
from main.tasks import samples
from main.tasks.samples.tags import SAMPLE_TAGS
from mentions.models import HCard, Webmention
from mentions.models.mixins import IncomingMentionType, MentionableMixin

now = datetime.now(tz=timezone.utc)

__all__ = [
    "HCardConfig",
    "create_about_page",
    "create_app",
    "create_app_type",
    "create_article",
    "create_blog",
    "create_changelog",
    "create_hcard",
    "create_language",
    "create_note",
    "generate_hcards",
    "generate_posts",
    "generate_webmentions_for",
]


def _any_or_none(qs: QuerySet):
    if not qs.exists():
        return None

    if random.random() > 0.5:
        items = list(qs)
        return random.choice(items)


def _timestamp(
    date: Optional[Date] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    second: Optional[int] = None,
) -> datetime:
    if date:
        year = date.year
        month = date.month
        day = date.day

    while True:
        dt = datetime(
            year=year or random.randint(2018, 2023),
            month=month or random.randint(1, 12),
            day=day or random.randint(1, 28),
            hour=hour or random.randint(0, 23),
            minute=minute or random.randint(0, 59),
            second=second or random.randint(0, 59),
            tzinfo=timezone.utc,
        )
        if dt <= now:
            return dt


def add_tags(obj: TaggableMixin):
    obj.tags.add(*random.sample(SAMPLE_TAGS, random.choice(range(1, 4))))


def create_article(
    title: str = None,
    tagline: str = "",
    preview_text: str = "",
    content: str = "",
    is_published: bool = True,
    tags: Optional[List[str]] = None,
    date: Optional[Date] = None,
) -> Article:
    sample = samples.any_post()
    created_at = _timestamp(date=date)

    article, _ = Article.objects.get_or_create(
        title=title or sample.title,
        defaults={
            "tagline": tagline or sample.summary,
            "preview_text": preview_text or sample.summary,
            "content": content or sample.content,
            "created_at": created_at,
            "published_at": created_at,
            "is_published": is_published,
        },
    )

    if tags:
        article.tags.add(*tags)

    return article


def create_blog(
    title: str = None,
    tagline: str = None,
    preview_text: str = None,
    content: str = None,
    is_published: bool = True,
    tags: Optional[List[str]] = None,
    date: Optional[Date] = None,
) -> Blog:
    sample = samples.any_post()
    created_at = _timestamp(date=date)

    blog, _ = Blog.objects.get_or_create(
        title=title or sample.title,
        defaults={
            "tagline": tagline or sample.summary,
            "preview_text": preview_text or sample.summary,
            "content": content or sample.content,
            "created_at": created_at,
            "published_at": created_at,
            "is_published": is_published,
        },
    )

    if tags:
        blog.tags.add(*tags)

    return blog


def create_note(
    content: Optional[str] = None,
    is_published: bool = True,
    tags: Optional[List[str]] = None,
    date: Optional[Date] = None,
) -> Note:
    note = Note.objects.create(
        content=content or samples.any_note(),
        published_at=_timestamp(date=date),
        is_published=is_published,
    )

    if tags:
        note.tags.add(*tags)

    return note


def create_app_type(
    name: Optional[str] = None,
    date: Optional[Date] = None,
) -> AppType:
    if not name:
        name = samples.any_app_type()

    app_type, _ = AppType.objects.get_or_create(
        name=name,
        defaults={
            "tooltip": name,
            "created_at": _timestamp(date=date),
        },
    )
    return app_type


def create_app(
    title: Optional[str] = None,
    app_id: Optional[str] = None,
    app_type: Optional[Union[AppType, str]] = None,
    language: Optional[str] = None,
    is_published: bool = True,
    tags: Optional[List[str]] = None,
    date: Optional[Date] = None,
) -> App:
    created_at = _timestamp(date=date)
    if not app_type:
        app_types = AppType.objects.all()
        if not app_types.exists():
            app_type = create_app_type()
        else:
            app_type = _any_or_none(app_types)

    if isinstance(app_type, str):
        app_type = create_app_type(app_type)

    if not title:
        title = samples.any_app_name()

    language = create_language(language)

    app, _ = App.objects.get_or_create(
        title=title,
        defaults={
            "app_id": app_id or slugify(title).replace("-", "."),
            "app_type": app_type,
            "created_at": created_at,
            "published_at": created_at,
            "is_published": is_published,
            "primary_language": language,
        },
    )

    if tags:
        app.tags.add(*tags)

    return app


def create_changelog(
    app: App = None,
    content: Optional[str] = None,
    version_name: Optional[str] = None,
    preview_text: Optional[str] = None,
    is_published: bool = True,
    tags: Optional[List[str]] = None,
    date: Optional[Date] = None,
) -> Changelog:
    created_at = _timestamp(date=date)

    if not app:
        app = create_app()

    sample = samples.any_changelog()

    changelog, _ = Changelog.objects.get_or_create(
        app=app,
        version_name=version_name or sample.version_name,
        defaults={
            "content": content or sample.content,
            "preview_text": preview_text or sample.summary,
            "created_at": created_at,
            "published_at": created_at,
            "is_published": is_published,
        },
    )

    if tags:
        changelog.tags.add(*tags)

    return changelog


def create_about_page(
    description: Optional[str] = None,
    content: Optional[str] = None,
) -> About:
    sample = samples.any_biography()

    about, _ = About.objects.get_or_create(
        description=description or sample.summary,
        content=content or sample.content,
    )
    return about


def generate_posts():
    funcs = [create_article, create_blog, create_note]
    for _ in range(0, 30):
        obj = random.choice(funcs)()
        add_tags(obj)

    for _ in range(0, 3):
        create_app_type()

    for _ in range(0, 10):
        app = create_app()
        add_tags(app)

    for _ in range(0, 20):
        changelog = create_changelog()
        add_tags(changelog)

    create_about_page()

    generate_hcards()
    generate_webmentions()


def generate_webmentions(force_hcard: bool = False, quote: Optional[str] = None):
    for m in implementations_of(MentionableMixin):
        for obj in m.objects.all():
            generate_webmentions_for(obj, force_hcard, quote)


def generate_webmentions_for(
    target: MentionableMixin,
    force_hcard: bool,
    quote: Optional[str],
):
    for n in range(3):
        hcard: HCard = HCard.objects.order_by("?").first()

        Webmention.objects.create(
            sent_by=hcard.homepage,
            approved=True,
            validated=True,
            hcard=hcard
            if force_hcard or random.random() > 0.3
            else None,  # Sometimes no hcard
            target_url=target.get_absolute_url(),
            source_url=urljoin(hcard.homepage, samples.any_urlpath()),
            post_type=random.choice(IncomingMentionType.serialized_names()),
            target_object=target,
            quote=quote,
        )


HCardConfig = namedtuple("HCardConfig", ["name", "homepage", "avatar"])


def create_hcard(card: Optional[HCardConfig] = None):
    if card:
        HCard.objects.create(
            name=card.name,
            homepage=card.homepage,
            avatar=card.avatar,
        )
    else:
        HCard.objects.create(
            name=samples.any_name(),
            homepage=samples.any_homepage(),
            avatar="https://i.pravatar.cc/64",  # Random avatar 64px in size
        )


def generate_hcards(
    cards: Optional[List[HCardConfig]] = None,
    count: int = 10,
):
    if cards:
        for card in cards:
            create_hcard(card)

    else:
        for n in range(count):
            create_hcard()
