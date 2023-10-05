import random

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from main.templatetags.repetition import repeat_until_length
from main.templatetags.strings import in_rainbows, nbsp
from main.util import apply_pipeline
from main.view_adapters import FeedItemContext

register = template.Library()


@register.filter("feedfilter_equals")
@stringfilter
def feedfilter_equals(self: str, arg: str) -> str:
    """Return "true" if all args are equal, "false" otherwise."""
    return str(self.lower() == arg.lower()).lower()


@register.simple_tag(name="choose_empty_feed_message")
@mark_safe
def choose_empty_feed_message() -> str:
    messages = [
        "Sorry about that",
        "My bad",
        "Sometimes I make mistakes",
        "I'm not much of a content creator",
        "oh no",
        '<span class="oh-no">oh&nbsp;<span class="marquee-wrapper"><span class="marquee">no no no no no no no no no no no no no no no NO</span></span></span>',
        "I'm sure they were here a minute ago",
        "Gradients are cool though, right?<br />&hellip;<i>right?</i>",
    ]

    message = random.choice(messages)
    return message


@register.filter("preview_image_text")
@mark_safe
def preview_image_text(item: FeedItemContext) -> str:
    text: str = item.title or item.summary

    pipeline = [
        (repeat_until_length, [60]),
        in_rainbows,
        nbsp,
    ]
    return apply_pipeline(text, pipeline)
