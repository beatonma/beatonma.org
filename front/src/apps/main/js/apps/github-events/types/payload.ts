import { Url } from "./common";

export type EventPayload = {};

export type CreateEventPayload = EventPayload & {
    type: string;
    ref: string;
};

export type IssueEventPayload = EventPayload & {
    number: number;
    url: Url;
    closed_at: string;
};

export type PullRequestPayload = EventPayload & {
    number: number;
    url: Url;
    merged_at: string;
    addition_count: number;
    deletion_count: number;
    changed_files_count: number;
};

export type PushPayload = EventPayload & Commit[];
export type Commit = {
    sha: string;
    message: string;
    url: Url;
};

export type WikiPayload = EventPayload & WikiEdit[];
export type WikiEdit = {
    name: string;
    url: Url;
    action: string;
};

export type ReleasePayload = EventPayload & {
    name: string;
    url: Url;
    description: string;
    published_at: string;
};
