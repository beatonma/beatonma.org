import re
from random import choice, random

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="startswith")
@stringfilter
def startswith(self: str, query: str) -> bool:
    if self is None:
        return False

    try:
        return self.startswith(query)
    except AttributeError:
        return str(self).startswith(query)


@register.filter(name="endswith")
@stringfilter
def endswith(self: str, query: str) -> bool:
    if self is None:
        return False

    try:
        return self.endswith(query)
    except AttributeError:
        return str(self).endswith(query)


@register.filter(name="remove")
@stringfilter
def remove(self: str, substring: str) -> str:
    if self is None:
        return ""

    return self.replace(substring, "")


@register.filter(name="in_rainbows")
@stringfilter
def in_rainbows(self: str):
    def _maybe(options: str) -> str:
        if random() > 0.9:
            return choice(options)
        return ""

    words = self.split(" ")
    for index, word in enumerate(words):
        if len(word) < 4:
            words[index] = f"{_maybe('_/')}{word}{_maybe('_/')}"
            continue

        words[index] = "".join([f"{x}{_maybe(' _/')}" for x in word])

    return " ".join(words)


@register.filter("nbsp")
@stringfilter
def nbsp(self: str):
    return self.replace(" ", "&nbsp;")


@register.filter("format")
@stringfilter
def stringformat(self: str, arg) -> str:
    """Replaces the first instance of {} with arg. Can be chained to replace multiple values."""
    return re.sub(r"{}", arg, self, count=1)
