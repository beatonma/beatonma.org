from datetime import datetime

from common.util.time import coerce_tzdatetime
from dateutil import parser as dateparser


def parse_datetime(text: str) -> datetime | None:
    if text is None:
        return None

    try:
        dt = dateparser.parse(text)
        return coerce_tzdatetime(dt)

    except TypeError:
        return None
