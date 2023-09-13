from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter("feedfilter_equals")
@stringfilter
def feedfilter_equals(self: str, arg: str) -> str:
    """Return "true" if all args are equal, "false" otherwise."""
    return str(self.lower() == arg.lower()).lower()
