from enum import StrEnum
from typing import List, Self


class GithubEvent(StrEnum):
    CreateEvent = "CreateEvent"
    WikiEvent = "GollumEvent"
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    PushEvent = "PushEvent"
    ReleaseEvent = "ReleaseEvent"

    @classmethod
    def values(cls) -> List[Self]:
        return list(map(lambda e: e.value, cls))
