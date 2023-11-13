"""Regular expressions that are used more than once."""
import re

# Match a #hashtag.
HASHTAG = re.compile(r"(?P<previous_token>^|>|\s)(?P<hashtag>#(?P<name>[-\w]+))")
