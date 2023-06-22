import logging

from django import template
from django.utils import dateformat, timezone

log = logging.getLogger(__name__)

register = template.Library()


@register.filter(name="minimaldate")
def hide_year(date) -> str:
    """If the date is the current year then remove the date"""
    if not date:
        return ""

    now = timezone.now()
    if date.year == now.year:
        return dateformat.format(date, "d N").replace(".", "")
    return dateformat.format(date, "d N Y").replace(".", "")


@register.filter(name="minimaltime")
def minimal_time(date) -> str:
    """Return a formatted timedelta since date."""
    if not date:
        return ""

    def _pluralized_message(quantity, one, many_or_zero):
        return f"{quantity} {one if quantity == 1 else many_or_zero} ago"

    now = timezone.now()
    delta = now - date

    days = delta.days
    if days > 30:
        return hide_year(date)
    elif days:
        return _pluralized_message(days, "day", "days")

    hours = round(delta.seconds / 3600)
    if hours:
        return _pluralized_message(hours, "hour", "hours")

    minutes = round(delta.seconds / 60)
    if minutes:
        return _pluralized_message(minutes, "minute", "minutes")

    seconds = delta.seconds % 60
    if seconds:
        return _pluralized_message(seconds, "second", "seconds")

    return hide_year(date)
