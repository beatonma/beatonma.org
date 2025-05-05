"""Default values for settings that are applied in all contexts.

These may still be overriden by the usual settings configuration - this is
just to provide reasonable set of defaults for stuff that basically never
needs to change."""

from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.parent.parent

# Django
APPEND_SLASH = True
ROOT_URLCONF = "beatonma.urls"
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TEST_RUNNER = "basetest.testrunner.PytestTestRunner"

# 1st-party apps
BMA_FEED_ITEMS_PER_PAGE = 10

# 3rd-party apps
TAGGIT_CASE_INSENSITIVE = True
