import { Repository } from "./common";
import {
    Commit,
    CreateEventPayload,
    EventPayload,
    IssueEventPayload,
    PullRequestPayload,
    ReleasePayload,
    WikiEdit,
} from "./payload";

export const Events = {
    Create: "CreateEvent",
    Push: "PushEvent",
    PullRequest: "PullRequestEvent",
    Wiki: "GollumEvent",
    Issue: "IssuesEvent",
    Release: "ReleaseEvent",
    Private: "PrivateEventSummary",
};

export interface Event {
    type: string;
    created_at: string;
}

export interface PrivateEventSummary extends Event {
    event_count: number;
    repository_count: number;
    change_count: number;
}

export interface PublicEvent extends Event {
    id: string;
    repository: Repository;
    payload: EventPayload;
}

export const isPublicEvent = (event: Event): event is PublicEvent => {
    if (event === null) return false;
    return (event as PublicEvent).id !== undefined;
};

export const isPrivateEvent = (
    event: unknown
): event is PrivateEventSummary => {
    if (event === null) return false;
    return (event as Event).type === Events.Private;
};

export interface PublicGroup {
    repository: Repository;
    timestamp: Date;
    createEvents: CreateEventPayload[];
    pushEvents: Commit[];
    issueEvents: IssueEventPayload[];
    wikiEditEvents: WikiEdit[];
    releaseEvents: ReleasePayload[];
    pullEvents: PullRequestPayload[];
}
