from basetest.testcase import LocalTestCase
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from github.models import (GithubLanguage, GithubLicense, GithubRepository,
                           GithubUser)
from github.models.events import (GithubEventUpdateCycle,
                                  GithubIssueClosedPayload,
                                  GithubPullRequestMergedPayload,
                                  GithubReleasePublishedPayload,
                                  GithubUserEvent, GithubWikiPayload)
from github.tasks import update_events
from github.tasks.api_models import Event
from main.models import App, Changelog

SAMPLE_CREATE_EVENT = Event.model_validate(
    {
        "id": "20975491109",
        "type": "CreateEvent",
        "actor": {
            "id": 12682046,
            "login": "beatonma",
            "display_login": "beatonma",
            "gravatar_id": "",
            "url": "https://api.github.com/users/beatonma",
            "avatar_url": "https://avatars.githubusercontent.com/u/12682046?",
        },
        "repo": {
            "id": 179150364,
            "name": "beatonma/django-wm",
            "url": "https://api.github.com/repos/beatonma/django-wm",
        },
        "payload": {
            "ref": "2.3.0",
            "ref_type": "branch",
            "master_branch": "master",
            "description": "Automatic Webmention functionality for Django models",
            "pusher_type": "user",
        },
        "public": True,
        "created_at": "2022-03-28T14:53:54Z",
    }
)

SAMPLE_PUSH_EVENT = Event.model_validate(
    {
        "id": "20975676236",
        "type": "PushEvent",
        "actor": {
            "id": 12682046,
            "login": "beatonma",
            "display_login": "beatonma",
            "gravatar_id": "",
            "url": "https://api.github.com/users/beatonma",
            "avatar_url": "https://avatars.githubusercontent.com/u/12682046?",
        },
        "repo": {
            "id": 179150364,
            "name": "beatonma/django-wm",
            "url": "https://api.github.com/repos/beatonma/django-wm",
        },
        "payload": {
            "push_id": 9469019997,
            "size": 1,
            "distinct_size": 1,
            "ref": "refs/heads/master",
            "head": "302345e36907ff579b124f6a8f22e99eb07713f9",
            "before": "06cf7c4c04406e585f4399cfdfd858accab58548",
            "commits": [
                {
                    "sha": "56a069f54d5ce31852d17e9b060ff5217d91009d",
                    "author": {"email": "beatonma@gmail.com", "name": "Michael Beaton"},
                    "message": "2.3.0: Blah blah blah",
                    "distinct": False,
                    "url": "https://api.github.com/repos/beatonma/django-wm/commits/56a069f54d5ce31852d17e9b060ff5217d91009d",
                },
            ],
        },
        "public": True,
        "created_at": "2022-03-28T15:01:50Z",
    }
)

SAMPLE_PULLREQUEST_EVENT = Event.model_validate(
    {
        "id": "20950698922",
        "type": "PullRequestEvent",
        "actor": {
            "id": 12682046,
            "login": "beatonma",
            "display_login": "beatonma",
            "gravatar_id": "",
            "url": "https://api.github.com/users/beatonma",
            "avatar_url": "https://avatars.githubusercontent.com/u/12682046?",
        },
        "repo": {
            "id": 179150364,
            "name": "beatonma/django-wm",
            "url": "https://api.github.com/repos/beatonma/django-wm",
        },
        "payload": {
            "action": "closed",
            "number": 24,
            "pull_request": {
                "url": "https://api.github.com/repos/beatonma/django-wm/pulls/24",
                "id": 869344326,
                "node_id": "PR_kwDOCq2eHM4z0SRG",
                "html_url": "https://github.com/beatonma/django-wm/pull/24",
                "diff_url": "https://github.com/beatonma/django-wm/pull/24.diff",
                "number": 24,
                "state": "closed",
                "locked": False,
                "title": "Allow `published` to be overridden",
                "user": {},
                "body": "I'm migrating my site over to Wagtail and using django-wm to handle webmentions. \r\n\r\nWhilst running the content import I noticed that all the published dates for existing webmentions were set to today, because `published` is set to `auto_now_add=True`, which [can't be overridden](https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.DateField.auto_now_add). \r\n\r\nThere's already a `created_at` field set in `MentionsBaseModel` using `auto_now_add=True`. \r\n\r\nThis change sets `published` to `timezone.now` maintaining existing functionality but allowing the field to be overriden during an import.",
                "created_at": "2022-03-02T10:05:16Z",
                "updated_at": "2022-03-26T14:03:04Z",
                "closed_at": "2022-03-26T14:03:04Z",
                "merged_at": "2022-03-26T14:03:04Z",
                "merge_commit_sha": "d4d382aaf1ecd81c101711c2b7d96cc0667ab02e",
                "head": {},
                "base": {},
                "merged": True,
                "commits": 1,
                "additions": 2,
                "deletions": 1,
                "changed_files": 1,
            },
        },
        "public": True,
        "created_at": "2022-03-26T14:03:05Z",
    }
)

SAMPLE_RELEASE_EVENT = Event.model_validate(
    {
        "id": "20950698922",
        "type": "ReleaseEvent",
        "actor": {
            "id": 12682046,
            "login": "beatonma",
            "display_login": "beatonma",
            "gravatar_id": "",
            "url": "https://api.github.com/users/beatonma",
            "avatar_url": "https://avatars.githubusercontent.com/u/12682046?",
        },
        "repo": {
            "id": 179150364,
            "name": "octocat/Hello-World",
            "url": "https://api.github.com/repos/octocat/Hello-World",
        },
        "payload": {
            "action": "published",
            "changes": {},
            "release": {
                "url": "https://api.github.com/repos/octocat/Hello-World/releases/1",
                "html_url": "https://github.com/octocat/Hello-World/releases/v1.0.0",
                "assets_url": "https://api.github.com/repos/octocat/Hello-World/releases/1/assets",
                "upload_url": "https://uploads.github.com/repos/octocat/Hello-World/releases/1/assets{?name,label}",
                "tarball_url": "https://api.github.com/repos/octocat/Hello-World/tarball/v1.0.0",
                "zipball_url": "https://api.github.com/repos/octocat/Hello-World/zipball/v1.0.0",
                "discussion_url": "https://github.com/octocat/Hello-World/discussions/90",
                "id": 1,
                "node_id": "MDc6UmVsZWFzZTE=",
                "tag_name": "v1.0.0",
                "target_commitish": "master",
                "name": "v1.0.0",
                "body": "Description of the release",
                "draft": False,
                "prerelease": False,
                "created_at": "2013-02-27T19:35:32Z",
                "published_at": "2013-02-27T19:35:32Z",
                "author": {},
                "assets": [],
            },
        },
        "public": True,
        "created_at": "2022-03-26T14:03:05Z",
    }
)

SAMPLE_ISSUES_EVENT = Event.model_validate(
    {
        "id": "20950698727",
        "type": "IssuesEvent",
        "actor": {
            "id": 12682046,
            "login": "beatonma",
            "display_login": "beatonma",
            "gravatar_id": "",
            "url": "https://api.github.com/users/beatonma",
            "avatar_url": "https://avatars.githubusercontent.com/u/12682046?",
        },
        "repo": {
            "id": 179150364,
            "name": "beatonma/django-wm",
            "url": "https://api.github.com/repos/beatonma/django-wm",
        },
        "payload": {
            "action": "closed",
            "issue": {
                "url": "https://api.github.com/repos/beatonma/django-wm/issues/26",
                "repository_url": "https://api.github.com/repos/beatonma/django-wm",
                "labels_url": "https://api.github.com/repos/beatonma/django-wm/issues/26/labels{/name}",
                "comments_url": "https://api.github.com/repos/beatonma/django-wm/issues/26/comments",
                "events_url": "https://api.github.com/repos/beatonma/django-wm/issues/26/events",
                "html_url": "https://github.com/beatonma/django-wm/issues/26",
                "id": 1181100859,
                "node_id": "I_kwDOCq2eHM5GZis7",
                "number": 26,
                "title": "Expand the allowed versions of the required requests package?",
                "user": {},
                "labels": [],
                "state": "closed",
                "locked": False,
                "assignee": None,
                "assignees": [],
                "milestone": None,
                "comments": 0,
                "created_at": "2022-03-25T18:22:12Z",
                "updated_at": "2022-03-26T14:03:03Z",
                "closed_at": "2022-03-26T14:03:03Z",
                "author_association": "NONE",
                "active_lock_reason": None,
                "body": "Issue description and suchlike",
                "reactions": {},
                "timeline_url": "https://api.github.com/repos/beatonma/django-wm/issues/26/timeline",
                "performed_via_github_app": None,
            },
        },
        "public": True,
        "created_at": "2022-03-26T14:03:04Z",
    }
)

SAMPLE_WIKI_EVENT = Event.model_validate(
    {
        "id": "21143487061",
        "type": "GollumEvent",
        "actor": {
            "id": 12682046,
            "login": "beatonma",
            "display_login": "beatonma",
            "gravatar_id": "",
            "url": "https://api.github.com/users/beatonma",
            "avatar_url": "https://avatars.githubusercontent.com/u/12682046?",
        },
        "repo": {
            "id": 179150364,
            "name": "beatonma/django-wm",
            "url": "https://api.github.com/repos/beatonma/django-wm",
        },
        "payload": {
            "pages": [
                {
                    "page_name": "Home",
                    "title": "Home",
                    "summary": None,
                    "action": "created",
                    "sha": "0c991f93a25747a8ca9bacabbd913750f2aa4cbf",
                    "html_url": "https://github.com/beatonma/snommoc/wiki/Home",
                }
            ]
        },
        "public": True,
        "created_at": "2022-04-06T13:28:39Z",
    }
)


def _datetime(year, month, day, hour=0, minute=0, second=0):
    return timezone.datetime(
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

        App.objects.create(
            title="my-app",
            app_id="my.app",
            repository=repo,
        )

    def test_base_update_event(self):
        update_events._create_event(self.update_cycle, SAMPLE_CREATE_EVENT)

        event: GithubUserEvent = GithubUserEvent.objects.first()
        self.assertEqual(event.user.username, "beatonma")
        self.assertEqual(event.type, "CreateEvent")
        self.assertEqual(event.is_public, True)
        self.assertEqual(event.repository.name, "django-wm")

    def test_update_create_event(self):
        update_events._create_event(self.update_cycle, SAMPLE_CREATE_EVENT)
        event = GithubUserEvent.objects.first()

        event_data = event.create_event_data

        self.assertEqual(event_data.ref, "2.3.0")
        self.assertEqual(event_data.ref_type, "branch")

    def test_update_push_event(self):
        update_events._create_event(self.update_cycle, SAMPLE_PUSH_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "PushEvent")
        commit = event.commits.first()

        self.assertEqual(
            commit.sha,
            "56a069f54d5ce31852d17e9b060ff5217d91009d",
        )
        self.assertEqual(commit.message, "2.3.0: Blah blah blah")
        self.assertEqual(
            commit.url,
            "https://github.com/beatonma/django-wm/commits/56a069f54d5ce31852d17e9b060ff5217d91009d",
        )

    def test_update_pullrequest_event(self):
        update_events._create_event(self.update_cycle, SAMPLE_PULLREQUEST_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "PullRequestEvent")
        event_data: GithubPullRequestMergedPayload = event.pull_merged_data

        self.assertEqual(
            event_data.url, "https://github.com/beatonma/django-wm/pull/24"
        )
        self.assertEqual(event_data.number, 24)
        self.assertEqual(
            event_data.merged_at,
            _datetime(2022, 3, 26, 14, 3, 4),
        )
        self.assertEqual(event_data.additions_count, 2)
        self.assertEqual(event_data.deletions_count, 1)
        self.assertEqual(event_data.changed_files_count, 1)

    def test_release_event(self):
        update_events._create_event(self.update_cycle, SAMPLE_RELEASE_EVENT)

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
        update_events._create_event(self.update_cycle, SAMPLE_RELEASE_EVENT)
        self.assertEqual(1, Changelog.objects.count())
        changelog = Changelog.objects.first()

        self.assertEqual(changelog.title, "v1.0.0")
        self.assertEqual(changelog.content, "Description of the release")

    def test_issues_event(self):
        update_events._create_event(self.update_cycle, SAMPLE_ISSUES_EVENT)

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
        update_events._create_event(self.update_cycle, SAMPLE_WIKI_EVENT)

        event = GithubUserEvent.objects.first()
        self.assertEqual(event.type, "GollumEvent")
        event_data: GithubWikiPayload = event.wiki_changes.first()

        self.assertEqual(
            event_data.url,
            "https://github.com/beatonma/snommoc/wiki/Home",
        )
        self.assertEqual(event_data.action, "created")
        self.assertEqual(event_data.name, "Home")

    def tearDown(self) -> None:
        self.update_cycle.delete()

        self.teardown_models(
            GithubLanguage,
            GithubRepository,
            GithubUser,
            Changelog,
        )


class FlushCacheTests(LocalTestCase):
    def test_flush_caches(self):
        GithubEventUpdateCycle.objects.create(created_at=_datetime(2022, 3, 1))
        GithubEventUpdateCycle.objects.create(created_at=_datetime(2022, 3, 2))

        # This one is most recent -> should persist
        latest = GithubEventUpdateCycle.objects.create(
            created_at=_datetime(2022, 3, 3, 5)
        )
        GithubEventUpdateCycle.objects.create(created_at=_datetime(2022, 3, 2, 13))
        GithubEventUpdateCycle.objects.create(created_at=_datetime(2022, 3, 3))

        update_events._flush_caches()

        objs = GithubEventUpdateCycle.objects.all()
        self.assertEqual(objs.count(), 1)
        self.assertEqual(objs.first(), latest)

    def tearDown(self):
        self.teardown_models(GithubEventUpdateCycle)
