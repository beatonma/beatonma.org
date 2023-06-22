import os
from pathlib import Path

from . import environment


# Include additional templates from environment.TEMPLATE_ROOT, if available.
external_template_root = environment.TEMPLATE_ROOT
_generated_dirs = []
if external_template_root is not None and os.path.exists(external_template_root):
    external_template_root = Path(external_template_root)
    for name in os.listdir(external_template_root):
        dirpath = external_template_root / name / "templates"
        if os.path.exists(dirpath):
            _generated_dirs.append(str(dirpath))


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
            "templates/flatpages",
            *_generated_dirs,
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
