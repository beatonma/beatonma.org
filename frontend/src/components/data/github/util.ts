import {
  type GithubEvent,
  GroupedEventPayloads,
  GroupedEvents,
  GroupedPublicEvents,
  PrivateEvent,
  PublicEvent,
  isPrivateEvent,
} from "./types";

/**
 * Consecutive private events are already flattened in backend - here we just
 * need to combine consecutive public events from the same repository.
 */
export const groupEvents = (events: GithubEvent[]): GroupedEvents[] => {
  const grouped: GroupedEvents[] = [];

  let _public: PublicGroup | null = null;

  const handlePrivate = (event: PrivateEvent) => {
    if (_public) {
      grouped.push(_public);
      _public = null;
    }
    grouped.push({
      timestamp: Date.parse(event.created_at),
      repositoryCount: event.repository_count,
      eventCount: event.event_count,
      changeCount: event.change_count,
    });
  };
  const handlePublic = (event: PublicEvent) => {
    if (_public && _public.repository.id !== event.repository.id) {
      grouped.push(_public);
      _public = null;
    }
    if (!_public) {
      _public = new PublicGroup(event);
    }
    _public.append(event);
  };

  for (const event of events) {
    if (isPrivateEvent(event)) handlePrivate(event);
    else handlePublic(event);
  }

  if (_public) grouped.push(_public);

  return grouped;
};

class PublicGroup implements GroupedPublicEvents {
  repository;
  timestamp: number;
  events: GroupedEventPayloads;
  eventCount: number;

  constructor(event: PublicEvent) {
    this.repository = event.repository;
    this.timestamp = Date.parse(event.created_at);
    this.eventCount = 0;
    this.events = {
      create: [],
      push: [],
      pullRequest: [],
      issue: [],
      wiki: [],
      release: [],
    };
  }

  append(event: PublicEvent) {
    this.eventCount += 1;
    switch (event.type) {
      case "PushEvent":
        this.events.push.push(...event.payload);
        break;
      case "GollumEvent":
        this.events.wiki.push(...event.payload);
        break;
      case "CreateEvent":
        this.events.create.push(event.payload);
        break;
      case "PullRequestEvent":
        this.events.pullRequest.push(event.payload);
        break;
      case "ReleaseEvent":
        this.events.release.push(event.payload);
        break;
      case "IssuesEvent":
        this.events.issue.push(event.payload);
        break;
    }
  }
}
