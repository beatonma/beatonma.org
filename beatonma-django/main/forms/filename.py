import os
import uuid
from typing import List, Optional

from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


@deconstructible
class RandomFilename:
    def __init__(
        self,
        path: str,
        filename_literals: List[str],
        filename_attrs: List[str],
    ):
        self.directory = timezone.now().strftime(path)
        self.filename_attrs = filename_attrs
        self.filename_literals = filename_literals

    def __call__(self, instance, original_filename) -> str:
        parts = original_filename.split(".")
        ext = parts[-1]

        chunks: List[str] = ["-".join(self.filename_literals)]

        if not instance:
            # No instance attributes if instance is null
            pass

        elif self.filename_attrs:
            attrs = [getattr(instance, attr, None) for attr in self.filename_attrs]
            attrs = [x for x in attrs if x]

            chunks.append("-".join(attrs))

        else:
            slug = _get_slug(instance)
            if slug:
                chunks.append(slug[:20])

        uid = uuid.uuid4().hex[:6]
        chunks.append(uid)
        basename = "-".join(chunk for chunk in chunks if chunk)
        basename = slugify(basename[:30])

        return os.path.join(self.directory, f"{basename}.{ext}")

    def __eq__(self, other):
        return (
            self.directory == other.directory
            and self.filename_attrs == other.filename_attrs
            and self.filename_literals == other.filename_literals
        )


def _get_slug(instance) -> Optional[str]:
    slug = getattr(instance, "slug", None)
    if slug:
        return slug

    target = getattr(instance, "target_object", None)
    if target:
        return getattr(target, "slug", None)

    return None
