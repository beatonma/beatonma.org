from typing import Type

from common.views.mentionable import MentionableView
from django.shortcuts import get_object_or_404, render
from main.models import AppPost, ChangelogPost
from main.models.rewrite.post import BasePost, Post
from mentions.helpers import mentions_re_path


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


slug_re = r"(?P<slug>[-\w]+)"
frontend_urlpatterns = [
    post_view(Post).as_mentions_re_path(rf"posts/{slug_re}/?"),
    post_view(AppPost).as_mentions_re_path(rf"apps/{slug_re}/?"),
    post_view(ChangelogPost).as_mentions_re_path(rf"changelog/{slug_re}/?"),
]
