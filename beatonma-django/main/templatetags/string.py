import math

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


@register.filter(name="repeat")
@stringfilter
def repeat(content: str, repeats: int, separator: str = " ") -> str:
    return separator.join([f"{content}{separator}" * repeats])


@register.filter(name="repeat_until_length")
@stringfilter
def repeat_until_length(content: str, target_length: int) -> str:
    chars = len(content)
    return repeat(content, math.ceil(target_length / chars))[:target_length]
