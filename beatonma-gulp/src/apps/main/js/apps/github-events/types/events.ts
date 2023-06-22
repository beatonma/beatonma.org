import { Repository } from "./common";
import { EventPayload } from "./payload";

export const Events = {
    Create: "CreateEvent",
    Push: "PushEvent",
    PullRequest: "PullRequestEvent",
    Wiki: "GollumEvent",
    Issue: "IssuesEvent",
    Release: "ReleaseEvent",
};

export interface Event {
    type: string;
    created_at: string;
}

export type PrivateEvent = Event;

export type PublicEvent = Event & {
    id: string;
    repository: Repository;
    payload: EventPayload;
};

export const isPublicEvent = (event: Event): event is PublicEvent => {
    if (event === null) return false;
    return (event as PublicEvent).id !== undefined;
};

export const isPrivateEvent = (event: Event): event is PrivateEvent => {
    if (event === null) return false;
    return !isPublicEvent(event);
};
