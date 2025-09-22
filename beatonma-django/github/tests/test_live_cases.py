from basetest.testcase import LocalTestCase
from github.models import GithubEventUpdateCycle
from github.tasks.update_events import _try_create_event
from github.tests import sampledata


class LiveTestCase(LocalTestCase):
    """Test specific situations that have occurred in the wild."""

    def setUp(self):
        user = sampledata.get_sample_user()
        repo = sampledata.get_sample_repository(
            id=1061228491,
            name="beatonma/gclocks-multiplatform",
            is_private=True,
            owner=user,
        )

    def test_no_create_event_data(self):
        data = [
            {
                "id": "54987975636",
                "type": "CreateEvent",
                "actor": {
                    "id": 12682046,
                    "login": "beatonma",
                    "display_login": "beatonma",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/beatonma",
                    "avatar_url": "",
                },
                "repo": {
                    "id": 1061228491,
                    "name": "beatonma/gclocks-multiplatform",
                    "url": "https://api.github.com/repos/beatonma/gclocks-multiplatform",
                },
                "payload": {
                    "ref": "main",
                    "ref_type": "branch",
                    "master_branch": "main",
                    "description": None,
                    "pusher_type": "user",
                },
                "public": False,
                "created_at": "2025-09-21T14:01:13Z",
            },
            {
                "id": "54987964327",
                "type": "CreateEvent",
                "actor": {
                    "id": 12682046,
                    "login": "beatonma",
                    "display_login": "beatonma",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/beatonma",
                    "avatar_url": "",
                },
                "repo": {
                    "id": 1061228491,
                    "name": "beatonma/gclocks-multiplatform",
                    "url": "https://api.github.com/repos/beatonma/gclocks-multiplatform",
                },
                "payload": {
                    "ref": None,
                    "ref_type": "repository",
                    "master_branch": "main",
                    "description": None,
                    "pusher_type": "user",
                },
                "public": False,
                "created_at": "2025-09-21T14:00:37Z",
            },
        ]

        update_cycle = GithubEventUpdateCycle.objects.create()

        event_one = _try_create_event(data[0], update_cycle)
        self.assertEqual(event_one.payload().ref_type, "branch")

        event_two = _try_create_event(data[1], update_cycle)
        self.assertEqual(event_two.payload().ref_type, "repository")
