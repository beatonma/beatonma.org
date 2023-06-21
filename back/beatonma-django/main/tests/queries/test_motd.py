from basetest.testcase import LocalTestCase
from common.util.time import tzdatetime
from main.models import MessageOfTheDay


class MotdTests(LocalTestCase):
    def test_get_current_is_correct(self):
        MessageOfTheDay.objects.create(
            created_at=tzdatetime(2023, 3, 15, 12, 0),
            is_published=False,
            content="not displayed",
        )

        MessageOfTheDay.objects.create(
            created_at=tzdatetime(2023, 3, 15, 12, 15),
            is_published=True,
            content="displayed but superseded",
        )

        MessageOfTheDay.objects.create(
            created_at=tzdatetime(2023, 3, 15, 12, 20),
            is_published=True,
            content="correct",
        )

        self.assertEqual(MessageOfTheDay.objects.get_current().content, "correct")

    def test_public_from(self):
        MessageOfTheDay.objects.create(
            created_at=tzdatetime(2023, 3, 15, 12, 20),
            content="correct",
            is_published=True,
            public_from=tzdatetime(2023, 3, 15, 12, 30),
        )

        self.assertIsNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 25))
        )
        self.assertIsNotNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 30))
        )

    def test_public_until(self):
        MessageOfTheDay.objects.create(
            created_at=tzdatetime(2023, 3, 15, 12, 20),
            content="correct",
            is_published=True,
            public_until=tzdatetime(2023, 3, 15, 12, 30),
        )

        self.assertIsNotNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 25))
        )
        self.assertIsNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 30))
        )

    def test_public_from_until(self):
        MessageOfTheDay.objects.create(
            created_at=tzdatetime(2023, 3, 15, 12, 20),
            content="correct",
            is_published=True,
            public_from=tzdatetime(2023, 3, 15, 12, 25),
            public_until=tzdatetime(2023, 3, 15, 12, 30),
        )

        self.assertIsNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2022, 3, 15, 12, 20))
        )

        self.assertIsNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 23))
        )

        self.assertIsNotNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 25))
        )
        self.assertIsNotNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 26))
        )
        self.assertIsNotNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 29))
        )

        self.assertIsNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2023, 3, 15, 12, 30))
        )
        self.assertIsNone(
            MessageOfTheDay.objects.get_for_datetime(tzdatetime(2024, 5, 15, 12, 30))
        )
