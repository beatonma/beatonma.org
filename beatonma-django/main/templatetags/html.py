import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

html_tag_pattern = re.compile(r"<.*?/?>")


@register.filter("plaintext")
@stringfilter
def plaintext(html: str) -> str:
    return re.sub(html_tag_pattern, "", html)


@register.filter("notetext")
@stringfilter
@mark_safe
def notetext(html: str) -> str:
    """Strip HTML tags, except <a>links</a>."""
    pattern = re.compile(r"<(?!/?a\s*[^>]*>)[^>]*>")
    return re.sub(pattern, "", html)
