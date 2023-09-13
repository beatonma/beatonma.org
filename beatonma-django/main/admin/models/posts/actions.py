from django.contrib import admin


@admin.action(description="Mark as public")
def action_publish(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Mark as private")
def action_unpublish(modeladmin, request, queryset):
    queryset.update(is_published=False)


PUBLISH_ACTIONS = [
    action_publish,
    action_unpublish,
]
