from django import template

register = template.Library()


@register.simple_tag(name="style")
def style(key: str, value) -> str:
    if not value:
        return ""

    return f"{key}:{value};"
