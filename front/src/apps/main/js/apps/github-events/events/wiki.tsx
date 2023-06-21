import React from "react";
import { AppIcon } from "../../../components/icons";
import { WikiEdit } from "../types";
import { Repository } from "../types/common";
import { GithubUrl } from "../urls";
import { Badge } from "./badge";

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
