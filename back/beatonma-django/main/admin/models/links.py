from django.contrib.contenttypes.admin import GenericTabularInline

from main.models import Link


class LinkInline(GenericTabularInline):
    model = Link
