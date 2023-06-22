import React from "react";
import { ReleasePayload } from "../types";

interface ReleaseEventsProps {
    events: ReleasePayload[];
}
export const ReleaseEvents = (props: ReleaseEventsProps) => {
    return (
        <>
            {props.events.map((event, index) => (
                <ReleaseEvent key={index} release={event} />
            ))}
        </>
    );
};

interface ReleaseProps {
    release: ReleasePayload;
}
const ReleaseEvent = (props: ReleaseProps) => {
    const release = props.release;

    return (
        <div>
            Release: <a href={release.url}>{release.name}</a>
        </div>
    );
};
