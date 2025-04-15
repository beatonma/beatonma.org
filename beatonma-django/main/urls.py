from common.urls import path
from mentions.helpers import mentions_path

from .api.rss import LatestUpdatesFeed
from .urls_frontend import frontend_urlpatterns
from .views import view_names
from .views.about import AboutView
from .views.app import AppView
from .views.index import IndexView
from .views.search import (
    AllAppsView,
    FilteredAppsView,
    LanguageView,
    SearchView,
    TagView,
)
from .views.webapp import WebAppView
from .views.webpost import ArticleView, BlogView, ChangelogView, NoteView

api_urlpatterns = [
    # RSS feed
    path("feed/", LatestUpdatesFeed(), view_names.RSS_FEED),
]

app_urlpatterns = [
    # Display info about an app.
    mentions_path(
        "app/<str:app_id>/",
        AppView.as_view(),
        name=view_names.APP,
        model_class="main.App",
    ),
    # Display preview of all apps.
    path("apps/", AllAppsView, view_names.ALL_APPS),
    path(
        "apps/<str:app_type>/",
        FilteredAppsView,
        view_names.APPS_BY_TYPE,
    ),
    # Render a instance of a webapp.
    path("webapp/<slug:slug>/", WebAppView, view_names.WEBAPP),
    # Redirect to changelog entry on app page.
    mentions_path(
        "changelog/<slug:slug>/",
        ChangelogView.as_view(),
        name=view_names.CHANGELOG,
        model_class="main.Changelog",
    ),
]

article_urlpatterns = [
    # Display an article
    mentions_path(
        "a/<slug:slug>/",
        ArticleView.as_view(),
        name=view_names.ARTICLE,
        model_class="main.Article",
    ),
    mentions_path(
        "blog/<slug:slug>/",
        BlogView.as_view(),
        name=view_names.BLOG,
        model_class="main.Blog",
    ),
    mentions_path(
        "note/<slug:slug>/",
        NoteView.as_view(),
        name=view_names.NOTE,
        model_class="main.Note",
    ),
]


site_functions_urlpatterns = [
    path("", IndexView, view_names.INDEX),
    path("about/", AboutView, view_names.ABOUT),
    path("tag/<str:tag>/", TagView, view_names.TAGS),
    path("language/<str:language>/", LanguageView, view_names.LANGUAGES),
    path("search/", SearchView, view_names.SEARCH),
]

urlpatterns = (
    api_urlpatterns
    + frontend_urlpatterns
    # + app_urlpatterns
    # + article_urlpatterns
    # + site_functions_urlpatterns
)
