import navigation
from common.models import SortableMixin
from django.core.exceptions import ValidationError
from django.db import models
from main.models.posts.post import BasePost, PostQuerySet


class AboutQuerySet(PostQuerySet):
    def root(self):
        return self.published().filter(parent__isnull=True).first()


class AboutPost(SortableMixin, BasePost):
    queryset_class = AboutQuerySet

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        related_query_name="child",
    )
    path = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self) -> str:
        return navigation.about(slug=self.slug if self.parent else None)

    def save(self, *args, **kwargs):
        qs = AboutPost.objects.all()

        try:
            root_pk = qs.get(slug="root").pk
        except AboutPost.DoesNotExist:
            root_pk = None

        if (not qs.exists()) or root_pk == self.pk:
            # Enforce values on root
            if self.parent:
                raise ValidationError("root post must not have a parent")

            self.title = ""
            self.slug = "root"
            self._update_path(save=False)
            super().save(*args, **kwargs, update_fields=None)
            return

        # Non-root
        if not self.parent:
            raise ValidationError("Non-root posts must have a parent")

        self._validate_ancestors(root_pk=root_pk)

        if not self.slug:
            self.slug = self.build_slug()

        super().save(*args, **kwargs)
        self._update_path(save=True)

    def _update_path(self, save: bool):
        existing = self.path
        if self.parent is None:
            self.path = ""
        else:
            self.path = self.parent.path + self.slug + "/"

        if save and self.path != existing:
            super().save(update_fields=["path"])

            # Apply changes to descendants
            for child in self.children.all():
                child._update_path(save=True)

    def _validate_ancestors(self, root_pk: int):
        """Raises ValidationError if loops or self-references are found in this object's ancestry."""
        seen_pks: set[int] = {self.pk}
        node = self.parent
        max_depth = 50
        depth = 0

        while True:
            if node.pk == root_pk:
                break

            if node.parent is None:
                raise ValidationError(
                    f"Post ancestors are not related to root! {node} does not have a parent."
                )

            if node.pk in seen_pks:
                raise ValidationError("Loop detected in post ancestors.")

            seen_pks.add(node.pk)
            node = node.parent
            depth += 1
            if depth >= max_depth:
                raise ValidationError("Ancestor tree validation reached its max_depth")
