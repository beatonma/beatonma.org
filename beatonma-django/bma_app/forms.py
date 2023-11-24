import logging

from django import forms
from django.core.exceptions import ValidationError

log = logging.getLogger(__name__)


class CreateNoteForm(forms.Form):
    token = forms.CharField(max_length=36, required=True)
    content = forms.CharField(required=False)
    file = forms.FileField(required=False)
    file_description = forms.CharField(max_length=140, required=False)

    def clean(self):
        cleaned_data = super().clean()

        content = cleaned_data.get("content")
        file = cleaned_data.get("file")

        if content:
            content = content.strip()
            cleaned_data["content"] = content

        if not content and not file:
            raise ValidationError(
                f"At least one of content({content is not None}), "
                f"file({file is not None}) must be provided."
            )

        return cleaned_data
