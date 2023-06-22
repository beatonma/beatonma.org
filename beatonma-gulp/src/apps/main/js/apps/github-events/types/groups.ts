import {
    Commit,
    CreateEventPayload,
    IssueEventPayload,
    PullRequestPayload,
    ReleasePayload,
    WikiEdit,
} from "./payload";
import { PrivateEvent } from "./events";
import { Repository } from "./common";

export interface Group {}

export type PrivateGroup = Group & {
    timestamp: Date;
    events: PrivateEvent[];
};

export type PublicGroup = Group & {
    repository: Repository;
    timestamp: Date;
    createEvents: CreateEventPayload[];
    pushEvents: Commit[];
    issueEvents: IssueEventPayload[];
    wikiEditEvents: WikiEdit[];
    releaseEvents: ReleasePayload[];
    pullEvents: PullRequestPayload[];
};

export const isPublicGroup = (group: Group): group is PublicGroup => {
    if (group === null) return false;
    return (group as PublicGroup).repository !== undefined;
};

export const isPrivateGroup = (group: Group): group is PrivateGroup => {
    if (group === null) return false;
    return !isPublicGroup(group);
};
