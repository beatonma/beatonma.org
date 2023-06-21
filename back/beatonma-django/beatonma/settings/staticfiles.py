from pathlib import Path

from . import BASE_DIR, environment

STATIC_URL = "/static/"
STATIC_ROOT = environment.STATIC_ROOT

_staticfiles_root = Path(environment.STATICFILES_ROOT or BASE_DIR)
STATICFILES_DIRS = (
    _staticfiles_root / "main/static/main/",
    _staticfiles_root / "dashboard/static/dashboard/",
    _staticfiles_root / "webapp/static/",
)
