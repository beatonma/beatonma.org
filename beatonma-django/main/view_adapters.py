from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FeedItemContext:
    """Passed to feed template."""

    title: str
    url: str
    date: datetime
    type: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    image_class: Optional[str] = None
    themeable: Optional["ThemeableMixin"] = None
