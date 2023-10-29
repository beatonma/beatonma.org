import { Time } from "../../components/datetime";
import { AppIcon, IconWithText } from "../../components/icon";
import {
    Commits,
    CreateEvents,
    IssueEvents,
    MergedPullRequests,
} from "./events";
import { WikiEvents } from "./events/wiki";
import { pluralize, PluralKey } from "./plurals";
import { isPrivateEvent, PrivateEventSummary, PublicGroup } from "./types";
import React from "react";

export const EventGroup = (group: PublicGroup | PrivateEventSummary) => {
    if (isPrivateEvent(group)) {
        return <PrivateSummary {...group} />;
    }
    return <PublicEventGroup {...group} />;
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

const PrivateSummary = (summary: PrivateEventSummary) => {
    const { event_count, repository_count, change_count } = summary;

    const buildString = (key: PluralKey, count: number, join: string = " ") =>
        `${count}${join}${pluralize(key, count)}`;

    const eventText = buildString("event", event_count);
    const repositoryText = buildString(
        "repository",
        repository_count,
        " private ",
    );
    const commitText = buildString("commit", change_count);

    let text: string;
    if (change_count === 0) {
        text = `${eventText} in ${repositoryText}.`;
    } else {
        text = `${eventText}/${commitText} in ${repositoryText}.`;
    }

    return (
        <div className="github-group">
            <div className="private">
                <IconWithText icon={AppIcon.Private} text={text} />
            </div>
        </div>
    );
};
