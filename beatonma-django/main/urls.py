from typing import Type

from common.urls import path
from common.views.mentionable import MentionableView
from django.shortcuts import get_object_or_404, render
from main.models import AppPost, ChangelogPost
from main.models.posts.post import BasePost, Post
from mentions.helpers import mentions_re_path

from .api.rss import LatestUpdatesFeed
from .views import view_names


def post_view(model_class: Type[BasePost]):
    class _View(MentionableView):
        reverse_name = model_class.qualified_name()

        def get(self, request, slug: str):
            post = get_object_or_404(model_class, slug=slug)
            return render(
                request,
                "post.html",
                {"post": post},
            )

        @classmethod
        def as_mentions_re_path(cls, route: str):
            return mentions_re_path(
                route,
                cls.as_view(),
                name=cls.reverse_name,
                model_class=model_class.qualified_name(),
                model_filter_map={"slug": "slug"},
            )

    return _View


_slug_re = r"(?P<slug>[-\w]+)"

""" Used only to help django-wm resolve URLs to model instances - these are not
actually exposed publicly."""
frontend_urlpatterns = [
    post_view(Post).as_mentions_re_path(rf"posts/{_slug_re}/?"),
    post_view(AppPost).as_mentions_re_path(rf"apps/{_slug_re}/?"),
    post_view(ChangelogPost).as_mentions_re_path(rf"changelog/{_slug_re}/?"),
]


urlpatterns = [
    # RSS feed
    path("feed/", LatestUpdatesFeed(), view_names.RSS_FEED),
] + frontend_urlpatterns
