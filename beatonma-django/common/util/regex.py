"""Regular expressions that are used more than once."""
import re

# Match a #hashtag.
HASHTAG = re.compile(
    r"(?P<previous_token>^|>|\s)(?P<hashtag>#(?![a-fA-F0-9]{3})(?P<name>[-\w]+))(?=$|[\s.!?<])(?!\s*{)"
)
