import React from "react";
import { Time } from "../../components/datetime";
import { AppIcon, TextWithIcon } from "../../components/icons";
import { pluralize } from "./plurals";
import {
    Commits,
    CreateEvents,
    IssueEvents,
    MergedPullRequests,
} from "./events";
import { WikiEvents } from "./events/wiki";
import {
    Group,
    isPrivateGroup,
    isPublicGroup,
    PrivateGroup,
    PublicGroup,
} from "./types";

export const EventGroup = (group: Group) => {
    if (isPublicGroup(group)) {
        return <PublicEventGroup {...group} />;
    } else if (isPrivateGroup(group)) {
        return <PrivateEventGroup {...group} />;
    } else {
        throw `Unexpected group type: ${group}`;
    }
};

const PublicEventGroup = (group: PublicGroup) => {
    const repo = group.repository;

    return (
        <div className="github-group">
            <div className="github-group-header">
                <div className="github-repository-name">
                    <a href={repo.url}>{repo.name}</a>
                </div>
                <Time dateTime={group.timestamp.toISOString()} />
            </div>

            <div className="github-event-badges">
                <IssueEvents events={group.issueEvents} />
                <MergedPullRequests events={group.pullEvents} />
                <CreateEvents events={group.createEvents} repo={repo} />
                <WikiEvents edits={group.wikiEditEvents} repo={repo} />
            </div>

            <Commits commits={group.pushEvents} />
        </div>
    );
};

const PrivateEventGroup = (group: PrivateGroup) => {
    const count = group.events.length;
    return (
        <div className="github-group">
            <div className="private">
                <TextWithIcon
                    icon={AppIcon.Private}
                    text={`${count} ${pluralize(
                        "event",
                        count
                    )} in private repositories.`}
                />
            </div>
        </div>
    );
};
