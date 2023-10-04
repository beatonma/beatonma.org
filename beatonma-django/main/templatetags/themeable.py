from django import template
from main.models.mixins import ThemeableMixin
from main.views.util.color import generate_color_variants

register = template.Library()


@register.simple_tag(name="css_attr")
def css_attr(key: str, value) -> str:
    if not value:
        return ""

    return f"{key}:{value};"


@register.simple_tag(name="item_theme")
def item_theme(obj: ThemeableMixin) -> str:
    if not isinstance(obj, ThemeableMixin):
        return ""

    vibrant = obj.color_vibrant

    if not vibrant:
        return ""

    variants = generate_color_variants(vibrant)

    return "".join(
        [
            css_attr("--vibrant", variants.base),
            css_attr("--surface", variants.base),
            css_attr("--on-surface", variants.on_base),
        ]
    )
