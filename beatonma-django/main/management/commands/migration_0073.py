import os.path

from django.contrib.contenttypes.models import ContentType
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import models, transaction
from main.models import (
    About,
    App,
    AppPost,
    Article,
    Blog,
    ChangelogPost,
    Link,
    Note,
    Post,
    RelatedFile,
    UploadedFile,
    WebApp,
)
from main.models.rewrite import AboutPost
from main.models.rewrite.app import AppResource
from mentions.models import SimpleMention, Webmention


class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.all().delete()
        AppPost.objects.all().delete()
        ChangelogPost.objects.all().delete()

        migrate_posts()


def migrate_posts():
    migrate_notes()
    migrate_blogs()
    migrate_articles()
    migrate_apps()
    migrate_webapps()
    migrate_about()


def migrate_blogs():
    for blog in Blog.objects.all():
        print(f"Blog: {blog}")
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
    create_redirect(old_post, post)

    post.tags.add(*list(old_post.tags.all().values_list("name", flat=True)))
    clone_webmentions(old_post, post)
    clone_related_files(old_post, post)
    clone_links(old_post, post)


def create_redirect(old, new):
    site = Site.objects.first()

    Redirect.objects.update_or_create(
        old_path=old.get_absolute_url(),
        site=site,
        defaults={"new_path": new.get_absolute_url()},
    )


def migrate_about():
    for page in About.objects.all():
        with transaction.atomic():
            AboutPost.objects.create(
                created_at=page.created_at,
                modified_at=page.modified_at,
                content=page.content,
                content_html=page.content_html,
                is_published=page.active,
            )


def migrate_articles():
    for article in Article.objects.all():
        print(f"Article: {article}")
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
                hero_image=(
                    UploadedFile.objects.create(file=cloned)
                    if (cloned := clone_file(article.hero_image))
                    else None
                ),
                hero_html=article.hero_html,
                color_muted=article.color_muted,
                color_vibrant=article.color_vibrant,
            )
            clone_related(article, post)


def migrate_notes():
    for note in Note.objects.all():
        print(f"Note: {note}")
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


def migrate_apps():
    apps = App.objects.all()

    for app in apps:
        print(f"App: {app}")
        with transaction.atomic():
            post = AppPost.objects.create(
                created_at=app.created_at,
                modified_at=app.modified_at,
                old_slug=app.slug,
                api_id=app.api_id,
                content=app.content,
                content_html=app.content_html,
                is_published=app.is_published,
                published_at=app.published_at,
                color_muted=app.color_muted,
                color_vibrant=app.color_vibrant,
                title=app.title,
                subtitle=app.tagline,
                preview_text=app.tagline,
                repository=app.repository,
                codename=app.app_id,
                icon=(
                    UploadedFile.objects.create(file=cloned)
                    if (cloned := clone_file(app.icon))
                    else None
                ),
            )
            clone_related(app, post)
            migrate_changelogs(app, post)


def migrate_webapps():
    webapps = WebApp.objects.all()

    for app in webapps:
        print(f"WebApp: {app}")
        with transaction.atomic():
            post = AppPost.objects.create(
                created_at=app.created_at,
                modified_at=app.modified_at,
                is_published=True,
                published_at=app.created_at,
                old_slug=f"webapp-{app.slug}",
                slug=f"webapp-{app.slug}",
                codename=f"webapp-{app.slug}",
                title=app.title,
                preview_text=app.description,
                content_html=app.description,
                script_html=app.content_html,
            )

            create_redirect(app, post)

            script = AppResource.objects.create(app=post, file=clone_file(app.file))
            post.script = script
            post.save(update_fields=["script"])

            for res in app.resources.all():
                if cloned := clone_file(res.file):
                    AppResource.objects.create(app=post, file=cloned)


def migrate_changelogs(source: App, target: AppPost):
    for change in source.changelogs.all():
        print(f"Changelog: {change}")
        post = ChangelogPost.objects.create(
            created_at=change.created_at,
            modified_at=change.modified_at,
            old_slug=change.slug,
            api_id=change.api_id,
            content=change.content,
            content_html=change.content_html,
            is_published=change.is_published,
            published_at=change.published_at,
            app=target,
            title=change.title,
            version=change.version_name,
            subtitle=change.tagline,
            preview_text=change.preview_text,
        )
        clone_related(change, post)


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
    try:
        with file.storage.open(source, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {source}")
        return None

    return ContentFile(data, name=name)


def clone_links(source, target):
    source_gfk, target_gfk = genericforeignkey(source, target)

    for link in Link.objects.filter(**source_gfk):
        Link.objects.update_or_create(
            **target_gfk,
            url=link.url,
            defaults={
                "description": link.description,
                "host": link.host,
            },
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
