const DjangoWM = {
    id: 179150364,
    name: "beatonma/django-wm",
    url: "https://github.com/beatonma/django-wm",
    description: "Automatic Webmention functionality for Django models",
    license: "gpl-3.0",
};

const Snommoc = {
    id: 188595195,
    name: "beatonma/snommoc",
    url: "https://github.com/beatonma/snommoc",
    description: "Data server for Commons app",
    license: null,
};

export const SampleEvents = [
    {
        id: "21143687162",
        type: "GollumEvent",
        repository: Snommoc,
        payload: [
            {
                name: "Home",
                url: "https://github.com/beatonma/snommoc/wiki/Home",
                action: "edited",
            },
        ],
    },
    {
        id: "21143616015",
        type: "GollumEvent",
        repository: Snommoc,
        payload: [
            {
                name: "Home",
                url: "https://github.com/beatonma/snommoc/wiki/Home",
                action: "created",
            },
        ],
    },
    {
        type: "CreateEvent",
    },
    {
        type: "CreateEvent",
    },
    {
        type: "PushEvent",
    },
    {
        type: "PushEvent",
    },
    {
        type: "PushEvent",
    },
    {
        type: "PushEvent",
    },
    {
        id: "20979984751",
        type: "CreateEvent",
        repository: DjangoWM,
        payload: {
            type: "tag",
            ref: "2.3.0",
        },
    },
    {
        id: "20975676236",
        type: "PushEvent",
        repository: DjangoWM,
        payload: [
            {
                sha: "56a069f54d5ce31852d17e9b060ff5217d91009d",
                message:
                    '2.3.0: Enabled custom url-to-object resolution.\n\nNew MentionableMixin classmethod: `resolve_from_url_kwargs(**url_kwargs)`\n- This method receives captured parameters from an `urlpatterns` path.\n- By default, it uses `<slug:slug>` to look up your object by a unique\n  `slug` field.\n- You can customize this by overriding the classmethod in your\n  MentionableMixin implementation\n\n  e.g.\n    ```python\n    # urls.py\n    urlpatterns = [\n        path(\n            fr"<int:year>/<int:month>/<int:day>/<slug:post_slug>/",\n            MyBlogPostView.as_view(),\n            name="my-blog",\n            kwargs={\n                "model_name": "myapp.MyBlog",\n            },\n        ),\n    ]\n\n    # models.py\n    class MyBlog(MentionableMixin, models.Model):\n        date = models.DateTimeField(default=timezone.now)\n        slug = models.SlugField()\n        content = models.TextField()\n\n        def all_text(self):\n            return self.content\n\n        def get_absolute_url(self):\n            return reverse(\n                "my-blog",\n                kwargs={\n                    "year": self.date.strftime("%Y"),\n                    "month": self.date.strftime("%m"),\n                    "day": self.date.strftime("%d"),\n                    "post_slug": self.slug,\n                }\n            )\n\n        @classmethod\n        def resolve_from_url_kwargs(cls, year, month, day, post_slug, **url_kwargs):\n            return cls.objects.get(\n                date__year=year,\n                date__month=month,\n                date__day=day,\n                slug=post_slug,\n            )\n\n    ```\n\n`mentions.resolution.get_model_for_url_path` now delegates to\n`MentionableMixin.resolve_from_url_kwargs` to resolve captured URL\nparameters to a model instance.',
                url: "https://api.github.com/repos/beatonma/django-wm/commits/56a069f54d5ce31852d17e9b060ff5217d91009d",
            },
        ],
    },
    {
        id: "20975675821",
        type: "PullRequestEvent",
        repository: DjangoWM,
        payload: {
            number: 29,
            url: "https://github.com/beatonma/django-wm/pull/29",
            merged_at: "2022-03-28T15:01:48Z",
            addition_count: 224,
            deletions_count: 36,
            changed_files_count: 8,
        },
    },
    {
        id: "20975675709",
        type: "IssuesEvent",
        repository: DjangoWM,
        payload: {
            number: 28,
            url: "https://github.com/beatonma/django-wm/issues/28",
            closed_at: "2022-03-28T15:01:48Z",
        },
    },
    {
        id: "20975491109",
        type: "CreateEvent",
        repository: DjangoWM,
        payload: {
            type: "branch",
            ref: "2.3.0",
        },
    },
    {
        id: "20953688283",
        type: "PushEvent",
        repository: {
            id: 188595195,
            name: "beatonma/commons",
            url: "https://github.com/beatonma/commons",
            description:
                "Rewrite of Commons for Android. Still in the early stages but under active development!",
            license: null,
        },
        payload: [
            {
                sha: "09f07a46210026fc7b8198c01d3a0a744148cdb7",
                message:
                    "Renamed themed... accessors, removing the `themed` prefix.",
                url: "https://api.github.com/repos/beatonma/commons/commits/09f07a46210026fc7b8198c01d3a0a744148cdb7",
            },
        ],
    },
    {
        id: "20950717828",
        type: "CreateEvent",
        repository: DjangoWM,
        payload: {
            type: "tag",
            ref: "2.2.0",
        },
    },
    {
        id: "20950698922",
        type: "PullRequestEvent",
        repository: DjangoWM,
        payload: {
            number: 24,
            url: "https://github.com/beatonma/django-wm/pull/24",
            merged_at: "2022-03-26T14:03:04Z",
            addition_count: 2,
            deletions_count: 1,
            changed_files_count: 1,
        },
    },
    {
        id: "20950698893",
        type: "PushEvent",
        repository: DjangoWM,
        payload: [
            {
                sha: "ecc4030adff0646a6d8a969a49cfb925989dcf0d",
                message:
                    "Version bump: 2.1.1\n\nFix: Test view defined in main urlpatterns.",
                url: "https://api.github.com/repos/beatonma/django-wm/commits/ecc4030adff0646a6d8a969a49cfb925989dcf0d",
            },
        ],
    },
];
