from main.models import ThemeOverride
from main.views.util import get_theme_context


def theme_override(request) -> dict:
    return get_theme_context(ThemeOverride.objects.get_current())
