import logging

from django import forms
from django.core.exceptions import ValidationError
from main.models import Note, RelatedFile

log = logging.getLogger(__name__)


class MediaAttachmentForm(forms.Form):
    file: forms.FileField
    file_description: forms.CharField


class CreateNoteForm(MediaAttachmentForm, forms.Form):
    published_at = forms.DateTimeField(required=False)
    content = forms.CharField(
        max_length=Note.max_length,
        strip=True,
        required=False,
    )
    is_published = forms.CharField()
    file = forms.FileField(required=False)
    file_description = forms.CharField(
        max_length=RelatedFile.description_max_length,
        strip=True,
        required=False,
    )

    def clean_is_published(self):
        is_published = self.cleaned_data.get("is_published")
        if isinstance(is_published, str):
            is_published = is_published.lower()
            if is_published == "true":
                return True
            if is_published == "false":
                return False
            raise forms.ValidationError(
                "is_published field must be a 'true' or 'false' string."
            )
        if isinstance(is_published, bool):
            return is_published

        raise ValidationError(f"Unexpected value is_published={is_published}")

    def clean(self):
        cleaned_data = super().clean()

        content = cleaned_data.get("content")
        file = cleaned_data.get("file")

        if not content and not file:
            raise ValidationError(
                f"At least one of content({content is not None}), "
                f"file({file is not None}) must be provided."
            )

        return cleaned_data


class AppendNoteMediaForm(MediaAttachmentForm, forms.Form):
    file = forms.FileField()
    file_description = forms.CharField(
        max_length=RelatedFile.description_max_length,
        strip=True,
        required=False,
    )
