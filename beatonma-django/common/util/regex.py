"""Regular expressions that are used more than once."""

import re

# Match a #hashtag.
HASHTAG = re.compile(
    r"(^|(?<=>|\s))"  # Only accept if previous char is start-of-line, whitespace or an HTML tag.
    r"(?P<hashtag>#"  # Capture group for (#hashtag)
    r"(?![a-fA-F0-9]{3})"  # Ignore hex color codes
    r"(?P<name>[a-zA-Z][-\w]*))"  # Must start with a letter - capture group for #(name)
    r"(?=$|[^\w])"  # Followed by end-of-line or non-word character
    r"(?!\s*{)"  # Ignore if followed by opening brace '{' - likely a CSS ID selector
)


# Match a Github issue (e.g.#34)
GITHUB_ISSUE = re.compile(
    r"(^|(?<=>|\s))"  # Only accept if previous char is start-of-line, whitespace or an HTML tag.
    r"#(?P<issue>\d+)"  # Capture group for #(issue)
    r"(?=$|[^\w])"  # Followed by end-of-line or non-word character
)
