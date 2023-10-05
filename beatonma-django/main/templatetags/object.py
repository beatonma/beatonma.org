from django import template

register = template.Library()


@register.filter(name="get_class")
def get_class(obj) -> str:
    return obj.__class__.__name__


@register.filter(name="hasattr")
def has_attribute(obj, attr: str) -> bool:
    return hasattr(obj, attr)
