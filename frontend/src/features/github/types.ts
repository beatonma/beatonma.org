import type {
  GithubCreatePayload,
  GithubIssuePayload,
  GithubPrivateEvent,
  GithubPullRequestPayload,
  GithubPushPayload,
  GithubRecentEvents,
  GithubReleasePayload,
  GithubWikiPayload,
} from "@/api/types";

export type GithubRecent = GithubRecentEvents;
export type GithubEvent = GithubRecent["events"][number];
export type PrivateEvent = GithubPrivateEvent;
export type PublicEvent = Exclude<GithubEvent, PrivateEvent>;
export type GithubRepository = PublicEvent["repository"];

export type GroupedPrivateEvents = {
  eventCount: number;
  repositoryCount: number;
  changeCount: number;
  timestamp: number;
};

export interface GroupedEventPayloads {
  create: GithubCreatePayload[];
  push: GithubPushPayload[];
  pullRequest: GithubPullRequestPayload[];
  issue: GithubIssuePayload[];
  wiki: GithubWikiPayload[];
  release: GithubReleasePayload[];
}
export interface GroupedPublicEvents {
  repository: PublicEvent["repository"];
  timestamp: number;
  eventCount: number;
  events: GroupedEventPayloads;
}
export type GroupedEvents = GroupedPrivateEvents | GroupedPublicEvents;

export function isPrivateEvent(event: GithubEvent): event is PrivateEvent {
  return event.type === "PrivateEventSummary";
}

export function isPrivateGroup(
  group: GroupedEvents,
): group is GroupedPrivateEvents {
  return !("repository" in group);
}
