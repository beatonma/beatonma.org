from django.contrib import admin

from main.admin.models.posts import fieldsets
from main.admin.models.posts.webpost import WebPostAdmin
from main.models import Blog


@admin.register(Blog)
class BlogAdmin(WebPostAdmin):
    fieldsets = fieldsets.webpost_default("Blog")
