import inspect
import logging
from typing import Iterator, Type

from django import forms
from django.apps import apps
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

log = logging.getLogger(__name__)


class AdminWidgets:
    text_class = "max-w-[min(100%,80ch)] w-full text-lg!"

    def textarea(self, classes: str = "", rows: int = 5, cols: int = 80):
        return forms.Textarea(
            attrs={
                "rows": rows,
                "cols": cols,
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
     - fields are read-only by default, unless they appear in `editable_fields`
     - fieldsets are automatically generated.
        - fields can be grouped by defining them in `field_groups`
        - editable and read-only fields appear in separate sets
     - field generator methods should have their name prefixed with _field_ -
       these will be automatically discovered and added to self.readonly_fields.
       e.g. def _field_mymethod(self, obj): return obj.name
    """

    save_on_top = True

    editable_fields: list[str] = []
    collapse_readonly: bool = True

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
        css = {"all": ["common/admin.css"]}

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        if self.readonly_fields:
            log.warning(
                f"Admin class `{self.__class__.__name__}.readonly_fields` is defined but will be ignored. Use "
                f"`editable_fields` instead."
            )

        main_fields, readonly_fields, generated_fields = self.init_fields(model)
        self.readonly_fields = readonly_fields + generated_fields

        if not self.fieldsets:
            self.fieldsets = (
                (None, {"fields": self._apply_field_groups(main_fields)}),
                (
                    "Read only",
                    {
                        "fields": self._apply_field_groups(readonly_fields),
                        "classes": [
                            f"{"collapse" if self.collapse_readonly else ''} visible!"  # 'collapse' django class clashes with tailwind
                        ],
                    },
                ),
            )
            self.fields = None

    def init_fields(self, model) -> tuple[list[str], list[str], list[str]]:
        """Get all fields for this model, ordered by `field_order`."""

        def _is_excluded_class(x):
            return any(
                isinstance(x, cls)
                for cls in [
                    GenericRelation,
                    models.ManyToManyRel,
                ]
            )

        fields = [x for x in model._meta.get_fields() if not _is_excluded_class(x)]
        editable_fields = self.editable_fields or []

        if editable_fields == ["*"]:
            main_fields = [x.name for x in fields if x.editable and not x.primary_key]
        else:
            main_fields = [*editable_fields]

        generated_fields = self._get_generated_fields()
        readonly_fields = [x.name for x in fields if x.name not in main_fields]

        def _get_sort_order(field_name):
            try:
                return self.field_order.index(field_name)
            except ValueError:
                return 1_000

        return (
            sorted(main_fields + generated_fields, key=_get_sort_order),
            sorted(readonly_fields, key=_get_sort_order),
            generated_fields,
        )

    def _get_generated_fields(self):
        prefix = "_field_"
        methods = [
            x
            for x in inspect.getmembers(self, predicate=inspect.ismethod)
            if x[0].startswith(prefix)
        ]

        return [x[0] for x in methods]

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
