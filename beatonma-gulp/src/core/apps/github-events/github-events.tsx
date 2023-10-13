import { Dropdown } from "../../components/dropdown";
import { LoadingSpinner } from "../../components/loading";
import { Api } from "../../global/api";
import { EventGroup } from "./group";
import {
    Event,
    PublicEvent,
    isPrivateEvent,
    Events,
    IssueEventPayload,
    PullRequestPayload,
    ReleasePayload,
    CreateEventPayload,
    PrivateEventSummary,
    isPublicEvent,
    PublicGroup,
} from "./types";
import { Repository } from "./types/common";
import { PushPayload, WikiPayload } from "./types/payload";
import React, { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

const CONTAINER = "#github_recent";

export const GithubEventsApp = async (dom: Document | Element) => {
    const container = dom.querySelector(CONTAINER);

    if (container) {
        const root = createRoot(dom.querySelector(CONTAINER));
        root.render(
            <StrictMode>
                <GithubEvents />
            </StrictMode>,
        );
    }
};

type Group = PublicGroup | PrivateEventSummary;
const GithubEvents = () => {
    const [groups, setGroups] = useState<Group[] | null>();

    useEffect(() => {
        Api.githubEvents()
            .then(filterEvents)
            .then(setGroups)
            .catch(err => {
                console.warn(`Failed to load github content: ${err}`);
                setGroups(null);
            });
    }, []);

    if (groups === undefined) {
        return <LoadingSpinner />;
    } else if (groups === null) {
        return null;
    } else {
        return (
            <Dropdown
                expandedDefault={true}
                header={
                    <a href="https://github.com/beatonma">
                        <h2>github/beatonma</h2>
                    </a>
                }
            >
                <div className="github-events">
                    {groups.map((group: Group, index: number) => (
                        <EventGroup key={index} {...group} />
                    ))}
                </div>
            </Dropdown>
        );
    }
};

export const filterEvents = (events: Event[]): Group[] => {
    const groups: Group[] = [];

    let previousEvent: Event = null;
    let previousTimestamp: Date = null;

    // Public events only
    let previousRepo: Repository = null;
    let createEvents: CreateEventPayload[] = [];
    let issueEvents: IssueEventPayload[] = [];
    let releaseEvents: ReleasePayload[] = [];
    let pullEvents: PullRequestPayload[] = [];
    let pushEvents: PushPayload = [];
    let wikiEditEvents: WikiPayload = [];

    const savePublicGroup = () => {
        groups.push({
            repository: previousRepo,
            timestamp: previousTimestamp,
            createEvents: createEvents,
            issueEvents: issueEvents,
            releaseEvents: releaseEvents,
            pullEvents: pullEvents,
            pushEvents: pushEvents,
            wikiEditEvents: wikiEditEvents,
        });

        createEvents = [];
        issueEvents = [];
        releaseEvents = [];
        pullEvents = [];
        pushEvents = [];
        wikiEditEvents = [];
        previousTimestamp = null;
    };

    const handlePublicEvent = (event: PublicEvent) => {
        if (
            isPublicEvent(previousEvent) &&
            previousRepo?.id !== event.repository?.id
        ) {
            savePublicGroup();
        }

        switch (event.type) {
            case Events.Create:
                createEvents.push(event.payload as CreateEventPayload);
                break;
            case Events.Issue:
                issueEvents.push(event.payload as IssueEventPayload);
                break;
            case Events.PullRequest:
                pullEvents.push(event.payload as PullRequestPayload);
                break;
            case Events.Release:
                releaseEvents.push(event.payload as ReleasePayload);
                break;
            case Events.Wiki:
                wikiEditEvents = wikiEditEvents.concat(
                    event.payload as WikiPayload,
                );
                break;

            case Events.Push:
                pushEvents = pushEvents.concat(
                    (event.payload as PushPayload).map(push => {
                        let msg = push.message
                            .replace(
                                /(https:\/\/[^\s]+\.[^\s]+)/g,
                                `<a href="$1">$1</a>`,
                            ) // Linkify links
                            .replace(
                                /#(\d+)/g,
                                `<a href="${event.repository.url}/issues/$1/">#$1</a>`,
                            ) // Linkify references to Github issues
                            .replace(/`([^\s]+)`/g, `<code>$1</code>`); // wrap text in `quotes` with code tags

                        if (msg.indexOf("\n\n") >= 0) {
                            // If msg has a title line, just use that.
                            msg = msg.split("\n\n")[0];
                        }

                        return {
                            sha: push.sha,
                            message: msg,
                            url: push.url,
                        };
                    }),
                );

                break;

            default:
                throw `Unhandled event type: ${event.type}`;
        }

        previousRepo = event.repository;
    };

    const handlePrivateEvent = (event: PrivateEventSummary) => {
        if (isPublicEvent(previousEvent)) {
            savePublicGroup();
        }

        groups.push(event);
        previousRepo = null;
    };

    events.forEach(event => {
        if (isPublicEvent(event)) {
            handlePublicEvent(event);
        } else if (isPrivateEvent(event)) {
            handlePrivateEvent(event);
        } else {
            throw "Unexpected event appears to be neither PublicEvent nor PrivateEvent";
        }

        previousTimestamp = new Date(event.created_at);
        previousEvent = event;
    });

    if (isPublicEvent(previousEvent)) {
        savePublicGroup();
    }

    return groups;
};
