import re
from random import choice, random

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="startswith")
@stringfilter
def startswith(text: str, query: str) -> bool:
    if text is None:
        return False

    try:
        return text.startswith(query)
    except AttributeError:
        return str(text).startswith(query)


@register.filter(name="endswith")
@stringfilter
def endswith(text: str, query: str) -> bool:
    if text is None:
        return False

    try:
        return text.endswith(query)
    except AttributeError:
        return str(text).endswith(query)


@register.filter(name="remove")
@stringfilter
def remove(text: str, substring: str) -> str:
    if text is None:
        return ""

    return text.replace(substring, "")


@register.filter(name="in_rainbows")
@stringfilter
def in_rainbows(text: str) -> str:
    """Break up the given text in the style of that album art."""

    def _maybe(options: str) -> str:
        if random() > 0.9:
            return choice(options)
        return ""

    words = text.split(" ")
    for index, word in enumerate(words):
        if len(word) < 4:
            words[index] = f"{_maybe('_/')}{word}{_maybe('_/')}"
            continue

        words[index] = "".join([f"{x}{_maybe(' _/')}" for x in word])

    return " ".join(words)


@register.filter("nbsp")
@stringfilter
def nbsp(text: str) -> str:
    """Replace normal space characters with non-breaking spaces."""
    return text.replace(" ", "&nbsp;")


@register.filter("format")
@stringfilter
def stringformat(self: str, arg) -> str:
    """Replaces the first instance of {} with arg. Can be chained to replace multiple values."""
    return re.sub(r"{}", arg, self, count=1)
