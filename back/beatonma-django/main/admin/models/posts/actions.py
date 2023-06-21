def action_publish(modeladmin, request, queryset):
    queryset.update(is_published=True)


def action_unpublish(modeladmin, request, queryset):
    queryset.update(is_published=False)


PUBLISH_ACTIONS = [
    action_publish,
    action_unpublish,
]
