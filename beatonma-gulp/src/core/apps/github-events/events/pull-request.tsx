import { AppIcon } from "../../../components/icon";
import { PullRequestPayload } from "../types";
import { Badge } from "./badge";
import React from "react";

interface PullRequestsProps {
    events: PullRequestPayload[];
}

export const MergedPullRequests = (props: PullRequestsProps) => {
    return (
        <>
            {props.events.map((event, index) => (
                <MergedPullRequest key={index} request={event} />
            ))}
        </>
    );
};

interface PullProps {
    request: PullRequestPayload;
}

const MergedPullRequest = (props: PullProps) => {
    const request = props.request;

    return (
        <Badge
            className="merge"
            url={request.url}
            icon={AppIcon.Merge}
            issue={request.number}
            title={`Merged PR #${request.number}`}
        />
    );
};
