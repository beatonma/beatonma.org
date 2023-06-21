from unittest import mock

from django.utils.timezone import datetime, get_current_timezone, timedelta

from basetest.testcase import LocalTestCase
from webmentions_tester.models import TemporaryMention, get_active_temporary_mentions


def create_with_submission_time(url, time):
    with mock.patch("django.utils.timezone.now", mock.Mock(return_value=time)):
        return TemporaryMention.objects.create(url=url)


class TemporaryMentionTests(LocalTestCase):
    def test_expiration(self):

        now = datetime(
            year=2022,
            month=1,
            day=14,
            hour=14,
            minute=0,
            second=0,
            tzinfo=get_current_timezone(),
        )
        m = create_with_submission_time("https://beatonma.org", now)

        self.assertFalse(m.is_expired(now + timedelta(minutes=1)))
        self.assertFalse(m.is_expired(now + timedelta(minutes=9)))

        self.assertTrue(m.is_expired(now + timedelta(minutes=11)))

    def test_get_active_temporary_mentions(self):
        now = datetime(
            year=2022,
            month=1,
            day=14,
            hour=14,
            minute=0,
            second=0,
            tzinfo=get_current_timezone(),
        )

        print(TemporaryMention.objects.all())

        for x in range(3):
            create_with_submission_time(f"https://beatonma.org/{x}/", now)
        for x in range(11):
            create_with_submission_time(
                f"https://beatonma.org/{x}/", now + timedelta(minutes=5)
            )

        self.assertEqual(
            14, get_active_temporary_mentions(now + timedelta(minutes=6)).count()
        )

        # After > 10 minutes, first 3 mentions should be expired
        self.assertEqual(
            11, get_active_temporary_mentions(now + timedelta(minutes=13)).count()
        )

        # After > 15 minutes, all mentions should be expired
        self.assertEqual(
            0, get_active_temporary_mentions(now + timedelta(minutes=16)).count()
        )

    def tearDown(self) -> None:
        TemporaryMention.objects.all().delete()
