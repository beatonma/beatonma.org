import os.path

from django.contrib.contenttypes.models import ContentType
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import models, transaction
from main.models import Article, Blog, Link, Note, Post, RelatedFile, UploadedFile
from mentions.models import SimpleMention, Webmention


class Command(BaseCommand):
    def handle(self, *args, **options):
        migrate_posts()


def migrate_posts():
    migrate_notes()
    migrate_blogs()
    migrate_articles()


def migrate_blogs():
    for blog in Blog.objects.all():
        with transaction.atomic():
            post = Post.objects.create(
                created_at=blog.created_at,
                modified_at=blog.modified_at,
                old_slug=blog.slug,
                api_id=blog.api_id,
                title=blog.title,
                subtitle=blog.tagline,
                preview_text=blog.preview_text,
                content=blog.content,
                content_html=blog.content_html,
                is_published=blog.is_published,
                published_at=blog.published_at,
                color_muted=blog.color_muted,
                color_vibrant=blog.color_vibrant,
            )
            clone_related(blog, post)


def clone_related(old_post, post):
    site = Site.objects.first()

    Redirect.objects.create(
        old_path=old_post.get_absolute_url(),
        new_path=post.get_absolute_url(),
        site=site,
    )

    post.tags.add(*list(old_post.tags.all().values_list("name", flat=True)))
    clone_webmentions(old_post, post)
    clone_related_files(old_post, post)
    clone_links(old_post, post)


def migrate_articles():
    for article in Article.objects.all():
        with transaction.atomic():
            post = Post.objects.create(
                created_at=article.created_at,
                modified_at=article.modified_at,
                old_slug=article.slug,
                api_id=article.api_id,
                title=article.title,
                subtitle=article.tagline,
                preview_text=article.preview_text,
                content="\n".join(
                    [x for x in [article.abstract, article.content] if x]
                ),
                content_html="\n".join(
                    [x for x in [article.abstract_html, article.content_html] if x]
                ),
                is_published=article.is_published,
                published_at=article.published_at,
                content_script=article.content_script,
                app=article.apps.first(),
                hero_image=(
                    UploadedFile.objects.create(file=clone_file(article.hero_image))
                    if article.hero_image
                    else None
                ),
                hero_html=article.hero_html,
                color_muted=article.color_muted,
                color_vibrant=article.color_vibrant,
            )
            clone_related(article, post)


def migrate_notes():
    for note in Note.objects.all():
        with transaction.atomic():
            post = Post.objects.create(
                created_at=note.created_at,
                modified_at=note.modified_at,
                old_slug=note.slug,
                api_id=note.api_id,
                content=note.content,
                content_html=note.content_html,
                is_published=note.is_published,
                published_at=note.published_at,
            )
            clone_related(note, post)


def clone_related_files(source, target):
    source_gfk, target_gfk = genericforeignkey(source, target)

    for rf in RelatedFile.objects.filter(**source_gfk):
        RelatedFile.objects.create(
            **target_gfk,
            created_at=rf.created_at,
            file=clone_file(rf.file),
            thumbnail=clone_file(rf.thumbnail),
            fit=rf.fit,
            original_filename=rf.original_filename,
            type=rf.type,
            description=rf.description,
        )


def clone_file(file: models.FileField | None) -> ContentFile | None:
    try:
        source = file.path
    except ValueError:
        return None

    name = os.path.basename(source)
    with file.storage.open(source, "rb") as f:
        data = f.read()

    return ContentFile(data, name=name)


def clone_links(source, target):
    source_gfk, target_gfk = genericforeignkey(source, target)

    for link in Link.objects.filter(**source_gfk):
        Link.objects.create(
            **target_gfk,
            url=link.url,
            description=link.description,
            host=link.host,
        )


def clone_webmentions(source, target):
    source_gfk, target_gfk = genericforeignkey(source, target)

    for wm in Webmention.objects.filter(**source_gfk):
        Webmention.objects.create(
            **target_gfk,
            created_at=wm.created_at,
            sent_by=wm.sent_by,
            target_url=wm.target_url,
            source_url=wm.source_url,
            quote=wm.quote,
            post_type=wm.post_type,
            published=wm.published,
            hcard=wm.hcard,
            approved=wm.approved,
            validated=wm.validated,
            has_been_read=wm.has_been_read,
            notes=wm.notes,
        )

        for wm in SimpleMention.objects.filter(**source_gfk):
            SimpleMention.objects.create(
                **target_gfk,
                created_at=wm.created_at,
                target_url=wm.target_url,
                source_url=wm.source_url,
                quote=wm.quote,
                post_type=wm.post_type,
                published=wm.published,
                hcard=wm.hcard,
            )


def genericforeignkey(source, target):
    source_ct = ContentType.objects.get_for_model(source.__class__)
    source_pk = source.pk

    target_ct = ContentType.objects.get_for_model(target.__class__)
    target_pk = target.pk

    return [
        {"content_type": source_ct, "object_id": source_pk},
        {"content_type": target_ct, "object_id": target_pk},
    ]
