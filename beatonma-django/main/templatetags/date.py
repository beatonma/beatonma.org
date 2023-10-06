import logging
from datetime import date as Date
from datetime import timedelta

from django import template
from django.utils import dateformat, timezone

log = logging.getLogger(__name__)

register = template.Library()


@register.filter(name="minimaldate")
def hide_year(date: Date) -> str:
    """If the date is the current year then remove the date"""
    if not date:
        return ""

    today = Date.today()

    if is_same_day(date, today):
        return "Today"

    yesterday = today - timedelta(days=1)
    if is_same_day(date, yesterday):
        return "Yesterday"

    if date.year == today.year:
        return dateformat.format(date, "d N").replace(".", "")
    return dateformat.format(date, "d N Y").replace(".", "")


def is_same_day(a: Date, b: Date) -> bool:
    return a.year == b.year and a.month == b.month and a.day == b.day
