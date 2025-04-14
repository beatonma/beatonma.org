import { ResponseOf, schemas } from "@/api";

export type GithubRecent = ResponseOf<"/api/github/recent/">;
export type GithubEvent = GithubRecent["events"][number];
export type PrivateEvent = schemas["GithubPrivateEvent"];
export type PublicEvent = Exclude<GithubEvent, PrivateEvent>;
export type GithubRepository = PublicEvent["repository"];

export type GroupedPrivateEvents = {
  eventCount: number;
  repositoryCount: number;
  changeCount: number;
  timestamp: number;
};

export interface GroupedEventPayloads {
  create: schemas["GithubPublicCreateEvent"]["payload"][];
  push: schemas["GithubPublicPushEvent"]["payload"];
  pullRequest: schemas["GithubPublicPullRequestEvent"]["payload"][];
  issue: schemas["GithubPublicIssueEvent"]["payload"][];
  wiki: schemas["GithubPublicWikiEvent"]["payload"];
  release: schemas["GithubPublicReleaseEvent"]["payload"][];
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
