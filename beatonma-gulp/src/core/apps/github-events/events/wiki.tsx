import { AppIcon } from "../../../components/icon";
import { WikiEdit } from "../types";
import { Repository } from "../types/common";
import { GithubUrl } from "../urls";
import { Badge } from "./badge";
import React from "react";

interface WikiEventProps {
    repo: Repository;
    edits: WikiEdit[];
}
export const WikiEvents = (props: WikiEventProps) => {
    const { edits, repo } = props;
    const count = edits.length;

    if (count === 0) return null;

    return (
        <Badge
            url={GithubUrl.wiki(repo)}
            icon={AppIcon.Wiki}
            title={`${count} wiki edits`}
        />
    );
};
