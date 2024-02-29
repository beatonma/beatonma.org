from datetime import datetime

from django.utils.timezone import get_current_timezone


def tzdatetime(
    year,
    month=None,
    day=None,
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
) -> datetime:
    return datetime(
        year,
        month,
        day,
        hour,
        minute,
        second,
        microsecond,
        tzinfo=get_current_timezone(),
    )
