from django.urls import path

from github import view_names
from github.views import GithubEventsView

urlpatterns = [
    path("github-events/", GithubEventsView.as_view(), name=view_names.GITHUB_EVENTS),
]
