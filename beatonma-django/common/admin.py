import logging
from typing import Iterator, Type

from django import forms
from django.apps import apps
from django.contrib import admin
from django.db import models
from django.db.models import URLField
from django.utils.safestring import mark_safe

log = logging.getLogger(__name__)


def clickable_url(attr: str):
    def _callable(obj):
        url = getattr(obj, attr)
        return mark_safe(f"""<a href="{url}">{url}</a>""")

    _callable.short_description = attr
    return _callable


class AdminWidgets:
    text_class = "max-w-[min(100%,80ch)] w-full text-lg!"

    def textarea(self, classes: str = ""):
        return forms.Textarea(
            attrs={
                "rows": 20,
                "cols": 80,
                "class": self._build_class(classes, self.text_class),
            }
        )

    def textinput(self, classes: str = ""):
        return forms.TextInput(
            attrs={"class": self._build_class(classes, self.text_class)}
        )

    @staticmethod
    def _build_class(*parts):
        return " ".join([x for x in parts if x])


class BaseAdmin(admin.ModelAdmin):
    """
    Defaults:
     - automatically shows all fields of the model.
     - fields are read-only by default, unless their appear in `editable_fields`
     - fieldsets are automatically generated.
        - fields can be grouped by defining them in `field_groups`
        - editable and read-only fields appear in separate sets
    """

    save_on_top = True

    editable_fields: list[str] = []

    """Non-exhaustive ordering of field priority.
    
    Fields included here will be sorted in the defined order, followed by any
    remaining fields which will use their default ordering (i.e. order of 
    definition in the model)
    """
    field_order: list[str] = []

    """Fields that will appear grouped together when fieldsets are generated."""
    field_groups: list[list[str]] = []

    widgets = AdminWidgets()
    formfield_overrides = {
        models.CharField: {
            "widget": widgets.textinput(),
        },
        models.TextField: {
            "widget": widgets.textarea(),
        },
    }

    class Media:
        # Enable tailwind classes
        js = ["https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"]

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        fields = self.init_fields(model)

        # Update editable_fields using ordering from field_order
        self.editable_fields = [x for x in fields if x in self.editable_fields]
        self.readonly_fields = [x for x in fields if x not in self.editable_fields]

        if not self.fieldsets:
            self.fieldsets = (
                (None, {"fields": self._apply_field_groups(self.editable_fields)}),
                (
                    "Read only",
                    {
                        "fields": self._apply_field_groups(self.readonly_fields),
                        "classes": [
                            "collapse visible!"  # 'collapse' django class clashes with tailwind
                        ],
                    },
                ),
            )
            self.fields = None

        # Make any read-only URL fields clickable
        url_fields = [
            x
            for x in (model._meta.fields or [])
            if isinstance(x, URLField) and x.name in self.readonly_fields
        ]

        for f in url_fields:
            clickable_name = f"_clickable_{f.name}"
            setattr(self, clickable_name, clickable_url(f.name))

            fields[fields.index(f.name)] = clickable_name
            self.readonly_fields[self.readonly_fields.index(f.name)] = clickable_name

    def init_fields(self, model):
        """Get all fields for this model, ordered by `field_order`."""
        fields = self.fields or []
        fields = list(fields) + [
            x.name for x in (model._meta.fields or []) if x.name not in fields
        ]

        def _get_sort_order(field_name: str):
            try:
                return self.field_order.index(field_name)
            except ValueError:
                return 1_000

        fields = sorted(fields, key=_get_sort_order)
        return fields

    def _apply_field_groups(
        self, fields: list[str]
    ) -> tuple[str | tuple[str, str], ...]:
        sets = fields.copy()

        for group in self.field_groups:
            fields_present = True
            for g in group:
                if not (g in fields):
                    fields_present = False
            if not fields_present:
                continue

            indices = [fields.index(x) for x in group]
            replace_index = min(*indices)
            sets[replace_index] = tuple(group)
            for x in group:
                try:
                    sets.remove(x)
                except ValueError:
                    pass

        return tuple(sets)


def get_module_models(module_name: str) -> Iterator[Type[models.Model]]:
    repository_config = apps.get_app_config(module_name)
    return repository_config.get_models()


def register_models_to_default_admin(
    module_name: str,
    default_admin: Type[admin.ModelAdmin] = BaseAdmin,
):
    """
    Any models in the module that have not already been registered will be registered with default_admin.
    """
    for model in get_module_models(module_name):
        if not admin.site.is_registered(model):
            admin.site.register(model, default_admin)


def register_model_to_default_admin(model: Type[models.Model], **options):
    admin.site.register(model, BaseAdmin, **options)


def _get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.

    This implementation moves the apps in 'priority_apps' to the top for easy access.
    """
    app_dict = self._build_app_dict(request, app_label)

    priority_apps = [
        "contact",
        "main",
        "flatpages",
        "github",
        "bma_app",
        "bma_dev",
    ]

    # Sort the apps alphabetically.
    app_list = sorted(
        [x for x in app_dict.values() if x["app_label"] in priority_apps],
        key=lambda x: priority_apps.index(x["app_label"]),
    ) + sorted(
        [x for x in app_dict.values() if x["app_label"] not in priority_apps],
        key=lambda x: x["name"].lower(),
    )

    # Sort the models alphabetically within each app.
    for app in app_list:
        app["models"].sort(key=lambda x: x["name"])

    return app_list


admin.AdminSite.get_app_list = _get_app_list
