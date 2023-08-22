import os
from pathlib import Path
from typing import List, Optional

from django.template.loader import engines as template_engines

from . import BASE_DIR, environment


def _get_external_templates() -> List[str]:
    # Include additional templates from environment.TEMPLATE_ROOT, if defined.
    external_template_root: Optional[str] = environment.TEMPLATE_ROOT
    if external_template_root is None or not os.path.exists(external_template_root):
        return []

    external_template_root: Path = Path(external_template_root)
    external_dirs = []
    for name in os.listdir(external_template_root):
        if name == "templates":
            dirpath = external_template_root / name
        else:
            dirpath = external_template_root / name / "templates"

        if dirpath.exists():
            external_dirs.append(str(dirpath))

    return external_dirs


def get_flatpage_templates() -> List[str]:
    dirs = []
    for engine in template_engines.all():
        flatpage_dirs = [os.path.join(x, "flatpages") for x in engine.template_dirs]
        dirs.extend(x for x in flatpage_dirs if os.path.exists(x))

    files = []
    for d in dirs:
        files.extend(
            f"flatpages/{os.path.basename(x)}" for x in Path(d).glob("*.html") if x
        )
    return files


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            *_get_external_templates(),
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.views.context_processors.theme_override",
                "main.views.context_processors.staff",
                "mentions.context_processors.unread_webmentions",
            ],
        },
    },
]
