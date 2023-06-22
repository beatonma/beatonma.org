CREATE_EVENT = "CreateEvent"
WIKI_EVENT = "GollumEvent"  # Wiki edits
ISSUES_EVENT = "IssuesEvent"
PULL_REQUEST_EVENT = "PullRequestEvent"
PUSH_EVENT = "PushEvent"
RELEASE_EVENT = "ReleaseEvent"


def all_events():
    return [
        CREATE_EVENT,
        PUSH_EVENT,
        ISSUES_EVENT,
        RELEASE_EVENT,
        WIKI_EVENT,
        PULL_REQUEST_EVENT,
    ]
