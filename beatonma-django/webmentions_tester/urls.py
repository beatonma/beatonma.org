from django.urls import path

from webmentions_tester import view_names
from webmentions_tester.views import TemporaryMentionsView, WebmentionsTesterView

urlpatterns = [
    path("", WebmentionsTesterView.as_view(), name=view_names.WEBMENTIONS_TESTER),
    path(
        "active/",
        TemporaryMentionsView.as_view(),
        name=view_names.API_WEBMENTIONS_TESTER,
    ),
]
