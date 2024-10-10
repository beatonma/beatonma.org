from pathlib import Path

from . import environment
from .defaults import BASE_DIR

STATIC_URL = "/static/"
STATIC_ROOT = environment.STATIC_ROOT

_staticfiles_root = Path(environment.STATICFILES_ROOT or BASE_DIR)
STATICFILES_DIRS = [
    _staticfiles_root / "main/static/main/",
    _staticfiles_root / "dashboard/static/dashboard/",
]
if environment.STATICFILES_ROOT:
    STATICFILES_DIRS.append(_staticfiles_root / "static")
