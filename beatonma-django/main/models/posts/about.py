from main.models.posts.post import BasePost, PostQuerySet


class AboutQuerySet(PostQuerySet):
    def get_current(self):
        return self.published().order_by("-created_at").first()


class AboutPost(BasePost):
    queryset_class = AboutQuerySet

    def get_absolute_url(self) -> str:
        return "/about/"

    def save(self, *args, **kwargs):
        if self.is_published:
            AboutPost.objects.exclude(pk=self.pk).filter(is_published=True).update(
                is_published=False
            )

        super().save(*args, **kwargs)
