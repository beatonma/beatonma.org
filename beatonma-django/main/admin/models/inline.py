from adminsortable2.admin import CustomInlineFormSetMixin, SortableInlineAdminMixin
from common.models.generic import generic_fk
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.db.models import Max
from django.db.models.functions import Coalesce
from main.admin.util import media_preview
from main.models import AppResource, Link, RelatedFile


class AppResourceInline(TabularInline):
    model = AppResource
    extra = 1


class _SortableGenericFormSet(CustomInlineFormSetMixin, BaseGenericInlineFormSet):
    """Replacement for adminsortable2.SortableGenericInlineAdminMixin which didn't seem to work as expected."""

    def get_queryset(self):
        return self.model.objects.filter(**generic_fk(self.instance))

    def get_max_order(self):
        return self.get_queryset().aggregate(
            max_order=Coalesce(Max(self.default_order_field), 0)
        )["max_order"]


class _SortableGenericInline(SortableInlineAdminMixin):
    formset = _SortableGenericFormSet


class LinkInline(_SortableGenericInline, GenericTabularInline):
    model = Link
    extra = 1


class RelatedFileInline(_SortableGenericInline, GenericStackedInline):
    model = RelatedFile
    extra = 1

    fields = (
        ("file", "get_preview", "thumbnail", "get_thumbnail"),
        ("fit", "description"),
    )
    readonly_fields = ("get_preview", "get_thumbnail")
    preview_style = "max-width:150px;max-height:150px;"

    @admin.display(description="Preview")
    def get_preview(self, related):
        return media_preview(related.file, self.preview_style)

    @admin.display(description="Preview")
    def get_thumbnail(self, related):
        return media_preview(related.thumbnail, self.preview_style)
