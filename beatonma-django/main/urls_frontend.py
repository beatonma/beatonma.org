from typing import Type

from common.views.mentionable import MentionableView
from django.shortcuts import get_object_or_404, render
from main.models import AppPost, ChangelogPost
from main.models.rewrite.post import BasePost, Post
from mentions.helpers import mentions_path


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
        def as_mentions_path(cls, route: str):
            return mentions_path(
                route,
                cls.as_view(),
                name=cls.reverse_name,
                model_class=model_class.qualified_name(),
            )

    return _View


frontend_urlpatterns = [
    post_view(Post).as_mentions_path("posts/<slug:slug>/"),
    post_view(AppPost).as_mentions_path("apps/<slug:slug>/"),
    post_view(ChangelogPost).as_mentions_path("changelog/<slug:slug>/"),
]
