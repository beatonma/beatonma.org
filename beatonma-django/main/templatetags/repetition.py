import math
import random

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="range")
def create_range(until):
    return range(0, until)


@register.filter(name="repeat")
@stringfilter
def repeat(content: str, repeats: int, separator: str = " ") -> str:
    return separator.join([f"{content}{separator}" * repeats])


@register.filter(name="repeat_until_length")
@stringfilter
def repeat_until_length(content: str, target_length: int) -> str:
    chars = len(content)
    return repeat(content, math.ceil(target_length / chars))[:target_length]


@register.filter(name="as_list")
def as_list(content):
    return [content]


@register.simple_tag(name="choose")
def choose(*args) -> str:
    return random.choice(args)
