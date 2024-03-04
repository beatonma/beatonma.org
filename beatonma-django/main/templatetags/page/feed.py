from random import choice, random

from common.util.pipeline import apply_pipeline
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from main.models.mixins import ThemeableMixin
from main.templatetags.string import repeat_until_length
from main.view_adapters import FeedItemContext
from main.views.util.color import generate_color_variants

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

    message = choice(messages)
    return message


@register.filter("preview_image_text")
@mark_safe
def preview_image_text(item: FeedItemContext) -> str:
    text: str = item.title or item.summary

    pipeline = [
        (repeat_until_length, [60]),
        _in_rainbows,
        _nbsp,
    ]
    return apply_pipeline(text, pipeline)


@register.simple_tag(name="item_theme")
def item_theme(obj: ThemeableMixin) -> str:
    if not isinstance(obj, ThemeableMixin):
        return ""

    vibrant = obj.color_vibrant

    if not vibrant:
        return ""

    variants = generate_color_variants(vibrant)

    return "".join(
        [
            _css_attr("--vibrant", variants.base),
            _css_attr("--surface", variants.base),
            _css_attr("--on-surface", variants.on_base),
        ]
    )


def _in_rainbows(text: str) -> str:
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


def _nbsp(text: str) -> str:
    """Replace normal space characters with non-breaking spaces."""
    return text.replace(" ", "&nbsp;")


def _css_attr(key: str, value) -> str:
    if not value:
        return ""

    return f"{key}:{value};"
