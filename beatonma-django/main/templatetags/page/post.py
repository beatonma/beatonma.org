import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from main.views import reverse
from taggit.models import Tag

register = template.Library()

html_tag_pattern = re.compile(r"<.*?/?>")


@register.filter("note_text")
@stringfilter
@mark_safe
def note_text(html: str) -> str:
    """Strip HTML tags, except <a>links</a>."""
    pattern = re.compile(r"<(?!/?a\s*[^>]*>)[^>]*>")
    return re.sub(pattern, "", html)


@register.filter(name="tag_url")
def tag_url(tag: Tag) -> str:
    return reverse.tag(tag)
