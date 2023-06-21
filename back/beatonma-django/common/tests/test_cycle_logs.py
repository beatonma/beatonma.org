from datetime import datetime, timedelta, timezone

from basetest.testcase import LocalTestCase
from common.models import PageView
from common.tasks.cycle_logs import cycle_logs

url = "https://beatonma.org/whatever/"
tz = timezone.utc


def _create_pageview(
    month: int,
    day: int,
    year: int = 2022,
    hour: int = 12,
    minute: int = 0,
    second: int = 0,
) -> PageView:
    """Excuse the American date format - it's actually useful here(!)"""
    return PageView.objects.create(
        created_at=datetime(year, month, day, hour, minute, second, tzinfo=tz),
        url=url,
    )


class CycleLogsTests(LocalTestCase):
    def setUp(self) -> None:
        _create_pageview(month=4, day=29)
        _create_pageview(month=4, day=30)
        _create_pageview(month=4, day=30)
        _create_pageview(month=5, day=21)

        _create_pageview(month=5, day=22)
        _create_pageview(month=5, day=22)
        _create_pageview(month=5, day=22)

    def test_cycle_logs(self):
        now = datetime(2022, 5, 31, 12, 0, 0, tzinfo=tz)
        older_than = timedelta(days=10)

        deleted_count, _ = cycle_logs(older_than=older_than, now=now)

        self.assertEqual(deleted_count, 4)
        self.assertEqual(PageView.objects.all().count(), 3)

    def tearDown(self) -> None:
        self.teardown_models(PageView)
