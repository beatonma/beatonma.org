from django import template

register = template.Library()


@register.simple_tag(name="equal")
def equal(*args) -> str:
    """Return "true" if all args are equal, "false" otherwise."""
    return str(args.count(args[0]) == len(args)).lower()
