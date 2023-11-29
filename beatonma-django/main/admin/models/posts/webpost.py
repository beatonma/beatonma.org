from common.admin import BaseAdmin
from django import forms
from main.admin.models.links import LinkInline
from main.admin.models.posts.actions import PUBLISH_ACTIONS
from main.admin.models.relatedfile import RelatedFileInline
from main.models.posts.webpost import RichWebPost


class WebPostAdminForm(forms.ModelForm):
    class Meta:
        model = RichWebPost
        fields = "__all__"


class WebPostAdmin(BaseAdmin):
    form = WebPostAdminForm

    readonly_fields = [
        "content_html",
        "created_at",
        "modified_at",
        "slug",
        "api_id",
    ]
    actions = PUBLISH_ACTIONS
    list_display = [
        "title",
        "is_published",
    ]
    list_filter = [
        "is_published",
        "published_at",
        "modified_at",
    ]
    search_fields = [
        "title",
        "preview_text",
        "tags",
    ]
    date_hierarchy = "published_at"
    inlines = [
        LinkInline,
        RelatedFileInline,
    ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # save_related is called after initial form.instance.save, so the tags
        # in the admin form will overwrite those extracted from the content
        # in BasePost.save. Here we combine both sources of tags.
        webpost = form.instance
        admin_form_tags = form.cleaned_data["tags"]

        webpost.tags.add(*admin_form_tags)
        webpost.save()
