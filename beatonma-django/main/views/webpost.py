import logging
from itertools import chain

from common.views.logged import LoggedView
from common.views.mentionable import MentionableView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from main.models import Article, Blog, Changelog, Note, Post

from ..models.link import sort_links
from . import view_names
from .util.color import get_theme_context

log = logging.getLogger(__name__)


_prefetch_fields = [
    "related_files",
    "tags",
]


class PostView(MentionableView):
    def get(self, request, slug: str):
        post = get_object_or_404(Post, slug=slug)

        return render(
            request,
            "post.html",
            {"post": post},
        )


class ArticleView(MentionableView, LoggedView):
    def get(self, request, slug: str):
        article = get_object_or_404(
            Article.objects.prefetch_related(
                "apps",
                "links",
                *_prefetch_fields,
            ),
            slug=slug,
        )
        apps = article.apps.all()
        links = chain(*[x.links.all() for x in apps], article.links.all())
        links = sort_links(links)

        return render(
            request,
            "pages/posts/article/article.html",
            {
                "post": article,
                "apps": apps,
                "links": links,
                **get_theme_context(article, apps.first()),
            },
        )


class BlogView(MentionableView, LoggedView):
    def get(self, request, slug: str):
        blog = get_object_or_404(
            Blog.objects.prefetch_related(
                *_prefetch_fields,
            ),
            slug=slug,
        )

        return render(
            request,
            "pages/posts/blog.html",
            {
                "post": blog,
                **get_theme_context(blog),
            },
        )


class NoteView(MentionableView, LoggedView):
    def get(self, request, slug: str):
        note = get_object_or_404(
            Note.objects.prefetch_related(
                *_prefetch_fields,
            ),
            slug=slug,
        )

        return render(
            request,
            "pages/posts/note/note.html",
            {
                "post": note,
            },
        )


class ChangelogView(MentionableView, LoggedView):
    def get(self, request, slug: str):
        """Redirect to app#changelog_id."""
        changelog = get_object_or_404(
            Changelog.objects.select_related("app").prefetch_related(
                *_prefetch_fields,
            ),
            slug=slug,
        )

        url = reverse(
            view_names.APP,
            kwargs={
                "app_id": changelog.app.app_id,
            },
        )
        url += "#" + changelog.slug
        return redirect(url)
