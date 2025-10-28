from datetime import datetime
from unittest.mock import patch

from django.utils.timezone import get_current_timezone

from basetest.testcase import LocalTestCase
from github import github_api
from github.models import GithubLanguage, GithubLicense, GithubRepository, GithubUser
from github.models.events import (
    GithubEventUpdateCycle,
    GithubIssueClosedPayload,
    GithubPullRequestMergedPayload,
    GithubReleasePublishedPayload,
    GithubUserEvent,
    GithubWikiPayload,
)
from github.tasks import update_events
from github.tests.testcase import MockJsonResponse
from main.models import AppPost, ChangelogPost

from . import update_events_testdata as testdata


def _datetime(year, month, day, hour=0, minute=0, second=0):
    return datetime(
        year,
        month,
        day,
        hour,
        minute,
        second,
        tzinfo=get_current_timezone(),
    )


class UpdateEventsTest(LocalTestCase):
    def setUp(self) -> None:
        self.now = _datetime(2022, 4, 4)
        self.update_cycle = GithubEventUpdateCycle.objects.create()

        owner = GithubUser.objects.create(
            id=12682046,
            username="beatonma",
            url="https://github.com/beatonma",
            avatar_url="",
        )

        repo = GithubRepository.objects.create(
            id=179150364,
            owner=owner,
            url="https://github.com/beatonma/django-wm",
            updated_at=self.now,
            name="django-wm",
            full_name="beatonma/django-wm",
            description="whatever",
            is_private=False,
            size_kb=123,
            primary_language=GithubLanguage.objects.create(name="Python"),
            license=GithubLicense.objects.create(
                name="GNU General Public License v3.0",
                key="gpl-3.0",
                url="https://api.github.com/licenses/gpl-3.0",
            ),
        )

        AppPost.objects.create(
            title="my-app",
            codename="my.app",
            repository=repo,
        )

    def test_base_update_event(self):
        update_events._create_event(self.update_cycle, testdata.SAMPLE_CREATE_EVENT)

        event: GithubUserEvent = GithubUserEvent.objects.first()
        self.assertEqual(event.user.username, "beatonma")
        self.assertEqual(event.type, "CreateEvent")
        self.assertEqual(event.is_public, True)
        self.assertEqual(event.repository.name, "django-wm")

    def test_update_create_event(self):
        update_events._create_event(self.update_cycle, testdata.SAMPLE_CREATE_EVENT)
        event = GithubUserEvent.objects.first()

        event_data = event.create_event_data

        self.assertEqual(event_data.ref, "2.3.0")
        self.assertEqual(event_data.ref_type, "branch")

    def test_update_push_event(self):
        with patch.object(
            github_api,
            "_get",
            side_effect=lambda request: MockJsonResponse(
                request, testdata.SAMPLE_PUSH_COMMITS_JSON
            ),
        ):
            update_events._create_event(self.update_cycle, testdata.SAMPLE_PUSH_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "PushEvent")

        self.assert_length(event.commits.all(), 7)

        first = event.commits.first()
        self.assertEqual(first.sha, "382de5ba4dca3aea9f3da4053ec499b15b5d8a45")
        self.assertEqual(first.message, "newest commit")

        last = event.commits.last()
        print(last, last.created_at, last.sha)
        self.assertEqual(last.sha, "30606892ad7918e079ec220215414eade38043c9")
        self.assertEqual(last.message, "oldest commit")
        self.assertEqual(
            last.url,
            "https://github.com/beatonma/django-wm/commit/30606892ad7918e079ec220215414eade38043c9",
        )

    def test_update_pullrequest_event(self):
        with patch.object(
            github_api,
            "_get",
            side_effect=lambda request: MockJsonResponse(
                request, testdata.SAMPLE_PULLREQUEST_JSON
            ),
        ):
            update_events._create_event(
                self.update_cycle, testdata.SAMPLE_PULLREQUEST_EVENT
            )

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "PullRequestEvent")
        event_data: GithubPullRequestMergedPayload = event.pull_merged_data

        self.assertEqual(event_data.url, "https://github.com/beatonma/django-wm/pull/8")
        self.assertEqual(event_data.number, 8)
        self.assertEqual(event_data.merged_at, _datetime(2025, 8, 2, 17, 12, 7))
        self.assertEqual(event_data.additions_count, 3)
        self.assertEqual(event_data.deletions_count, 3)
        self.assertEqual(event_data.changed_files_count, 1)

    def test_release_event(self):
        update_events._create_event(self.update_cycle, testdata.SAMPLE_RELEASE_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "ReleaseEvent")
        event_data: GithubReleasePublishedPayload = event.release_data

        self.assertEqual(
            event_data.url, "https://github.com/octocat/Hello-World/releases/v1.0.0"
        )
        self.assertEqual(event_data.name, "v1.0.0")
        self.assertEqual(event_data.description, "Description of the release")
        self.assertEqual(
            event_data.published_at,
            _datetime(2013, 2, 27, 19, 35, 32),
        )

    def test_release_event_creates_changelog(self):
        update_events._create_event(self.update_cycle, testdata.SAMPLE_RELEASE_EVENT)
        self.assertEqual(1, ChangelogPost.objects.count())
        changelog = ChangelogPost.objects.first()

        self.assertTrue("v1.0.0" in changelog.title)
        self.assertEqual(changelog.content, "Description of the release")

    def test_issues_event(self):
        update_events._create_event(self.update_cycle, testdata.SAMPLE_ISSUES_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "IssuesEvent")
        event_data: GithubIssueClosedPayload = event.issue_closed_data

        self.assertEqual(
            event_data.url,
            "https://github.com/beatonma/django-wm/issues/26",
        )
        self.assertEqual(event_data.number, 26)
        self.assertEqual(event_data.closed_at, _datetime(2022, 3, 26, 14, 3, 3))

    def test_wiki_event(self):
        update_events._create_event(self.update_cycle, testdata.SAMPLE_WIKI_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "GollumEvent")
        event_data: GithubWikiPayload = event.wiki_changes.first()

        self.assertEqual(
            event_data.url,
            "https://github.com/beatonma/snommoc/wiki/Home",
        )
        self.assertEqual(event_data.action, "created")
        self.assertEqual(event_data.name, "Home")
