import re

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
                    _preprocess_comments,
                    (
                        cls._preprocess_markdown,
                        [],
                        {"pipeline_extras": markdown_processors or []},
                    ),
                    cls._markdown_to_html,
                    _postprocess_comments,
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
                Html.flatten_contents,
                Html.linkify_html,
                Html.prettify_links,
            ],
        ).decode_contents()

    @classmethod
    def _markdown_to_html(cls, markdown: str) -> str:
        html = markdown2.markdown(
            markdown,
            extras=[
                "cuddled-lists",  # Don't require blank line before markdown lists
                "fenced-code-blocks",  # Use ``` instead of indent for code blocks
                "footnotes",
                "header-ids",
                "smarty-pants",  # Fancy quote marks and suchlike
                "spoiler",  # >! spoiler syntax
                "strike",  # ~~strikethrough~~
                "tables",
                "tag-friendly",  # Don't interpret `#tags` as `# headers`
                "task_list",  # - [x] checkboxes
                "xml",  # See _preprocess_comments, _postprocess_comments
            ],
        )
        return html


class FormatMixin(models.Model):
    class Meta:
        abstract = True

    format = models.PositiveSmallIntegerField(
        choices=Formats.choices,
        default=Formats.MARKDOWN,
    )


def _preprocess_comments(markdown: str) -> str:
    """Convert <!-- html comment syntax --> into <?xml instructions?> so they
    can pass through markdown formatting untouched. Required 'xml' extra to
    be enabled in markdown2."""
    return re.sub(r"<!-- (.+?) -->", r"\n\n<?COMMENT \1?>\n\n", markdown)


def _postprocess_comments(html: str) -> str:
    """Convert <?xml instructions?> back to <!-- html comments --> after
    other formatting is complete."""
    html = re.sub(
        r"\s*<\?COMMENT (.+?)\?>\s*", r"\n<!-- \1 -->\n", html, flags=re.MULTILINE
    )
    return html
