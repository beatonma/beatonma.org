import random
from collections import namedtuple
from datetime import date as Date
from datetime import datetime, timezone
from urllib.parse import urljoin

from common.models import TaggableMixin
from common.models.util import implementations_of
from django.db.models import QuerySet
from django.utils.text import slugify
from github.tests.sampledata import create_sample_language
from main.models import AboutPost, AppPost, ChangelogPost, MessageOfTheDay, Post
from main.tasks import samples
from main.tasks.samples.tags import SAMPLE_TAGS
from mentions.models import HCard, Webmention
from mentions.models.mixins import IncomingMentionType, MentionableMixin

now = datetime.now(tz=timezone.utc)

__all__ = [
    "HCardConfig",
    "create_about_page",
    "create_app",
    "create_changelog",
    "create_hcard",
    "create_sample_language",
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
    date: Date = None,
    year: int = None,
    month: int = None,
    day: int = None,
    hour: int = None,
    minute: int = None,
    second: int = None,
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


def create_post(
    title: str = None,
    subtitle: str = "",
    preview: str = "",
    content: str = "",
    is_published: bool = True,
    tags: list[str] = None,
    date: Date = None,
) -> Post:
    sample = samples.any_post()
    created_at = _timestamp(date=date)
    post, _ = Post.objects.get_or_create(
        title=title or sample.title,
        defaults={
            "subtitle": subtitle or sample.summary,
            "preview": preview or sample.summary,
            "content": content or sample.content,
            "is_published": is_published,
            "published_at": created_at,
            "created_at": created_at,
        },
    )
    if tags:
        post.tags.add(*tags)

    return post


def create_app(
    title: str = None,
    codename: str = None,
    is_published: bool = True,
    tags: list[str] = None,
    date: Date = None,
) -> AppPost:
    created_at = _timestamp(date=date)

    if not title:
        title = samples.any_app_name()

    app, _ = AppPost.objects.get_or_create(
        title=title,
        defaults={
            "codename": codename or slugify(title).replace("-", "."),
            "created_at": created_at,
            "published_at": created_at,
            "is_published": is_published,
        },
    )

    if tags:
        app.tags.add(*tags)

    return app


def create_changelog(
    app: AppPost = None,
    content: str = None,
    version: str = None,
    preview: str = None,
    is_published: bool = True,
    tags: list[str] = None,
    date: Date = None,
) -> ChangelogPost:
    created_at = _timestamp(date=date)

    if not app:
        app = create_app()

    sample = samples.any_changelog()

    changelog, _ = ChangelogPost.objects.get_or_create(
        app=app,
        version=version or sample.version_name,
        defaults={
            "content": content or sample.content,
            "preview": preview or sample.summary,
            "created_at": created_at,
            "published_at": created_at,
            "is_published": is_published,
        },
    )

    if tags:
        changelog.tags.add(*tags)

    return changelog


def create_about_page(
    description: str = None,
    content: str = None,
) -> AboutPost:
    sample = samples.any_biography()

    about, _ = AboutPost.objects.get_or_create(
        title=description or sample.summary,
        content=content or sample.content,
    )
    return about


def create_motd(
    title: str = None,
    content_html: str = None,
    is_published: bool = True,
) -> MessageOfTheDay:
    sample = samples.any_motd()

    motd, _ = MessageOfTheDay.objects.get_or_create(
        title=title or sample.title,
        content_html=content_html or sample.content,
        defaults={
            "is_published": is_published,
        },
    )
    return motd


def generate_posts():
    for _ in range(0, 30):
        obj = create_post()
        add_tags(obj)

    for _ in range(0, 10):
        app = create_app()
        add_tags(app)

    for _ in range(0, 20):
        changelog = create_changelog()
        add_tags(changelog)

    create_about_page()

    generate_hcards()
    generate_webmentions()


def generate_webmentions(force_hcard: bool = False, quote: str = None):
    for m in implementations_of(MentionableMixin):
        for obj in m.objects.all():
            generate_webmentions_for(obj, force_hcard, quote)


def generate_webmentions_for(
    target: MentionableMixin,
    force_hcard: bool,
    quote: str,
):
    for n in range(3):
        hcard: HCard = HCard.objects.order_by("?").first()

        Webmention.objects.create(
            sent_by=hcard.homepage,
            approved=True,
            validated=True,
            hcard=(
                hcard if force_hcard or random.random() > 0.3 else None
            ),  # Sometimes no hcard
            target_url=target.get_absolute_url(),
            source_url=urljoin(hcard.homepage, samples.any_urlpath()),
            post_type=random.choice([x.value for x in IncomingMentionType]),
            target_object=target,
            quote=quote,
        )


HCardConfig = namedtuple("HCardConfig", ["name", "homepage", "avatar"])


def create_hcard(card: HCardConfig = None):
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
    cards: list[HCardConfig] = None,
    count: int = 10,
):
    if cards:
        for card in cards:
            create_hcard(card)

    else:
        for n in range(count):
            create_hcard()
