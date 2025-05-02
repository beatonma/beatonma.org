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
                Html.remove_empty,
            ],
        ).decode_contents()

    @classmethod
    def _markdown_to_html(cls, markdown: str) -> str:
        html = markdown2.markdown(
            markdown,
            extras=[
                "cuddled-lists",  # Don't require blank line before markdown lists
                "fenced-code-blocks",  # Code syntax highlighting
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
    can pass through markdown formatting 'untouched'. Required 'xml' extra to
    be enabled in markdown2."""
    return re.sub(r"<!-- (.+?) -->", r"<?COMMENT \1?>\n\n", markdown)


def _postprocess_comments(html: str) -> str:
    """Convert <?xml instructions?> back to <!-- html comments --> after
    other formatting is complete."""

    replacements = [
        (
            # <!-- html comments -->
            r"(?:\n\n)?<\?COMMENT (.+?)\?>(?:\n\n)?",
            r"<!-- \1 -->",
        ),
        (
            # Escaped <!-- comments --> in ```code blocks```
            r"(?:\n\n)?&lt;\?COMMENT (.+?)\?&gt;(?:\n\n)?",
            r"&lt;!-- \1 --&gt;",
        ),
        (
            # <?Comment.Preproc?> -> <!-- Comment.Multiline -->
            r'(?:\n\n)?<span class="cp">(.*?)</span>(?:\n\n)?',
            r'<span class="cm">\1</span>',
        ),
    ]

    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, flags=re.MULTILINE)

    return html
