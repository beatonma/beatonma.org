from django import template

register = template.Library()


@register.filter(name="nullable")
def nullable(obj, attr: str):
    if obj:
        return getattr(obj, attr, None)
