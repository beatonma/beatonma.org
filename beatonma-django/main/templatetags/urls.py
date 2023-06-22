from django import template
from main.views import reverse
from taggit.models import Tag

register = template.Library()


@register.filter(name="tag_url")
def tag_url(tag: Tag) -> str:
    return reverse.tag(tag)
