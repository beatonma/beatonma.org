from django import template

register = template.Library()


@register.filter(name="hasattr")
def has_attribute(obj, attr: str):
    return hasattr(obj, attr)
