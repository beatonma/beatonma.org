import React from "react";
import { AppIcon } from "../../../components/icons";
import { IssueEventPayload } from "../types";
import { Badge } from "./badge";

interface IssueEventsProps {
    events: IssueEventPayload[];
}

export const IssueEvents = (props: IssueEventsProps) => {
    return (
        <>
            {props.events.map((event, index) => (
                <IssueEvent key={index} event={event} />
            ))}
        </>
    );
};

interface IssueProps {
    event: IssueEventPayload;
}

const IssueEvent = (props: IssueProps) => {
    const { url, number, ...rest } = props.event;

    return (
        <Badge
            className="issue"
            url={url}
            icon={AppIcon.Done}
            issue={number}
            title={`Closed issue #${number}`}
            {...rest}
        />
    );
};
