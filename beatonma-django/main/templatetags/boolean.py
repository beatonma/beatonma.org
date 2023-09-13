from django import template

register = template.Library()


@register.filter(name="negate")
def negate(value: bool) -> bool:
    return not value
