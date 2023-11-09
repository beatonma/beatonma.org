PUBLISHING = (
    "Publishing",
    {
        "fields": (
            ("allow_outgoing_webmentions",),
            ("is_published",),
        )
    },
)

THEME = (
    "Theme",
    {
        "fields": (
            "color_muted",
            "color_vibrant",
        ),
    },
)

METADATA = (
    "Metadata",
    {
        "classes": ("collapse",),
        "fields": (
            "slug",
            (
                "published_at",
                "created_at",
                "modified_at",
            ),
        ),
    },
)


def webpost_default(name: str):
    return (
        (
            name,
            {
                "fields": (
                    "title",
                    "tagline",
                    "preview_text",
                    (
                        "format",
                        "content",
                    ),
                    "tags",
                ),
            },
        ),
        PUBLISHING,
        THEME,
        METADATA,
        generated_html("content_html"),
    )


def generated_html(*fields):
    return (
        "Generated HTML",
        {
            "classes": ("collapse",),
            "fields": (*fields,),
        },
    )
