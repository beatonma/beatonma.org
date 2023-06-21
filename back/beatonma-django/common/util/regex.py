"""Regular expressions that are used more than once."""
import re

HASHTAG = re.compile(r"(^|>|\s)(#([-\w]+))")
