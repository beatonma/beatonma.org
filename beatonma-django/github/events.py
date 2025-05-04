from enum import StrEnum
from typing import Self


class GithubEvent(StrEnum):
    CreateEvent = "CreateEvent"
    WikiEvent = "GollumEvent"
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    PushEvent = "PushEvent"
    ReleaseEvent = "ReleaseEvent"

    @classmethod
    def values(cls) -> list[Self]:
        return list(map(lambda e: e.value, cls))
