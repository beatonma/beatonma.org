import React from "react";
import { AppIcon } from "../../../components/icons";
import { CreateEventPayload } from "../types";
import { Repository } from "../types/common";
import { GithubUrl } from "../urls";
import { Badge } from "./badge";

interface CreateEventsProps {
    repo: Repository;
    events: CreateEventPayload[];
}
export const CreateEvents = (props: CreateEventsProps) => {
    const { events, repo } = props;
    return (
        <>
            {events.map((event, index) => (
                <CreateEvent key={index} event={event} repo={repo} />
            ))}
        </>
    );
};

interface CreateProps {
    repo: Repository;
    event: CreateEventPayload;
}
const CreateEvent = (props: CreateProps) => {
    const { repo } = props;
    const { type, ref } = props.event;

    switch (type) {
        case "tag":
            return (
                <Badge
                    url={GithubUrl.tag(repo, ref)}
                    icon={AppIcon.Release}
                    text={ref}
                    title={`Created tag ${ref}`}
                />
            );

        case "branch":
            return (
                <Badge
                    url={GithubUrl.branches(repo)}
                    icon={AppIcon.Branch}
                    text={ref}
                    title={`Created branch ${ref}`}
                />
            );

        default:
            return null;
    }
};
