import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

html_tag_pattern = re.compile(r"<.*?/?>")


@register.filter("plaintext")
@stringfilter
def plaintext(html: str) -> str:
    return re.sub(html_tag_pattern, "", html)
