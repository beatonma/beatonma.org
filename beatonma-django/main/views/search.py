import logging
import random
from itertools import chain
from typing import List

from common.views.logged import LoggedView
from django.db.models import Count, F
from django.shortcuts import redirect, render
from github.models import GithubLanguage, GithubRepository
from main.views.querysets import (
    MAX_SUGGESTIONS,
    FeedMessage,
    get_app_types,
    get_apps,
    get_articles,
    get_blogs,
    get_languages,
    get_notes,
    get_repositories,
    get_search_results,
    get_suggestions,
)
from main.views.util import pluralize
from taggit.models import Tag

log = logging.getLogger(__name__)


class SearchView(LoggedView):
    def get(self, request):
        query = request.GET.get("query")
        if not query:
            return redirect("index")

        if query[:1] == "#":
            return redirect("search-tags", tag=query[1:])

        return render(
            request,
            "pages/search/search.html",
            {
                "filters": get_suggestions()[:MAX_SUGGESTIONS],
                **get_search_results(query),
            },
        )


class TagView(LoggedView):
    def get(self, request, tag: str):
        def _filter_tag(qs):
            return qs.filter(tags__name__iexact=tag)

        articles = _filter_tag(get_articles())
        blogs = _filter_tag(get_blogs())
        notes = _filter_tag(get_notes())
        apps = _filter_tag(get_apps())
        repositories = _filter_tag(get_repositories())

        results = list(chain(articles, blogs, apps, notes, repositories))

        private_repos_count = (
            GithubRepository.objects.get_private__dangerous__()
            .filter(tags__name__iexact=tag)
            .count()
        )

        if private_repos_count > 0:
            private_repos_message = FeedMessage(
                message=f"{private_repos_count} private {pluralize(private_repos_count, 'repository', 'repositories')}",
            )
            results += [private_repos_message]

        filters = list(
            Tag.objects.annotate(item_count=Count("taggit_taggeditem_items"))
            .exclude(item_count=0)
            .values_list("name", flat=True)
        )
        random.shuffle(filters)

        return render(
            request,
            "pages/search/tag.html",
            dict(
                filters=filters[:MAX_SUGGESTIONS],
                filter=tag,
                feed=results,
            ),
        )


class LanguageView(LoggedView):
    def get(self, request, language: str):
        resolved_language = (
            GithubLanguage.objects.filter(name__iexact=language).first()
            or GithubLanguage.objects.filter(name__icontains=language).first()
        )
        if not resolved_language:
            return self.render(request, language, [])

        apps = get_apps().filter(primary_language=resolved_language)
        repos = get_repositories().filter(primary_language=resolved_language)
        results = list(chain(apps, repos))

        private_repos_count = (
            GithubRepository.objects.get_private__dangerous__()
            .filter(primary_language=resolved_language)
            .count()
        )

        if private_repos_count > 0:
            private_repos_message = FeedMessage(
                message=f"{private_repos_count} private {pluralize(private_repos_count, 'repository', 'repositories')}",
            )
            results += [private_repos_message]

        return self.render(request, resolved_language.name, results)

    def render(self, request, language: str, results: List):
        filters = get_languages().values_list("name", flat=True)

        return render(
            request,
            "pages/search/language.html",
            dict(
                filters=filters,
                filter=language,
                feed=results,
            ),
        )


class AllAppsView(LoggedView):
    def get(self, request):
        apps = get_apps().order_by(F("published_at").desc(nulls_last=True))
        app_types = get_app_types().values_list("name", flat=True)

        return render(
            request,
            "pages/search/apps.html",
            dict(
                filters=app_types,
                feed=apps,
            ),
        )


class FilteredAppsView(LoggedView):
    def get(self, request, app_type: str):
        apps = get_apps().filter(app_type__name__iexact=app_type)
        app_types = get_app_types().values_list("name", flat=True)

        return render(
            request,
            "pages/search/apps.html",
            dict(
                filters=app_types,
                filter=app_type,
                feed=apps,
            ),
        )
