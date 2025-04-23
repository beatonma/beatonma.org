import markdown2
from bs4 import BeautifulSoup
from common.util.html import html_parser
from common.util.pipeline import PipelineItem, apply_pipeline
from django.db import models

from . import html as Html
from . import markdown as Markdown


class Formats(models.IntegerChoices):
    NONE = 0
    MARKDOWN = 1

    @classmethod
    def to_html(
        cls,
        format_: int,
        content: str,
        markdown_processors: list[PipelineItem[str]] = None,
        html_processors: list[PipelineItem[BeautifulSoup]] = None,
    ) -> str:
        if format_ == Formats.MARKDOWN:
            html = apply_pipeline(
                content,
                [
                    (
                        cls._preprocess_markdown,
                        [],
                        {"pipeline_extras": markdown_processors or []},
                    ),
                    cls._markdown_to_html,
                ],
            )
        else:
            html = content

        return cls._postprocess_html(html, html_processors)

    @classmethod
    def _preprocess_markdown(
        cls,
        markdown: str,
        pipeline_extras: list[PipelineItem[str]] = None,
    ) -> str:
        return apply_pipeline(
            markdown,
            [
                *(pipeline_extras or []),
                Markdown.apply_ligatures,
                Markdown.apply_blockquote_callout,
            ],
        )

    @classmethod
    def _postprocess_html(
        cls,
        html: str,
        pipeline_extras: list[PipelineItem[BeautifulSoup]] = None,
    ) -> str:
        soup = html_parser(html)

        return apply_pipeline(
            soup,
            [
                *(pipeline_extras or []),
                Html.linkify_html,
                Html.prettify_links,
            ],
        ).body.decode_contents()

    @classmethod
    def _markdown_to_html(cls, content: str) -> str:
        return markdown2.markdown(
            content,
            extras=[
                "cuddled-lists",
                "fenced-code-blocks",
                "footnotes",
                "header-ids",
                "smarty-pants",
                "spoiler",
                "strike",
                "tables",
                "tag-friendly",
            ],
        )


class FormatMixin(models.Model):
    class Meta:
        abstract = True

    format = models.PositiveSmallIntegerField(
        choices=Formats.choices,
        default=Formats.MARKDOWN,
    )
