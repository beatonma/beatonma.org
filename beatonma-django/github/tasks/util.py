from typing import Optional

from dateutil import parser as dateparser
from django.utils import timezone


def parse_datetime(text: str) -> Optional[timezone.datetime]:
    if text is None:
        return None

    try:
        # return _parse_datetime(text)
        dt = dateparser.parse(text)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
            parse_datetime(text)

        return dt

    except TypeError:
        return None
