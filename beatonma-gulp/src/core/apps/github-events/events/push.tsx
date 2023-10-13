import { Dropdown } from "../../../components/dropdown";
import { AppIcon, IconWithText } from "../../../components/icon";
import { pluralize } from "../plurals";
import { Commit } from "../types";
import React from "react";

interface CommitProps {
    commits: Commit[];
}

export const Commits = (props: CommitProps) => {
    const commits = props.commits;

    if (commits.length > 0) {
        return (
            <Dropdown
                className="github-event"
                data-type="commits"
                header={`${commits.length} ${pluralize(
                    "commit",
                    commits.length,
                )}`}
                expandedDefault={false}
            >
                {commits.map(commit => (
                    <CommitEvent key={commit.sha} {...commit} />
                ))}
            </Dropdown>
        );
    } else {
        return null;
    }
};

const CommitEvent = (commit: Commit) => {
    return (
        <IconWithText
            className="github-commit"
            icon={AppIcon.Link}
            iconClick={{
                href: commit.url,
                title: commit.url,
            }}
            dangerousHtml={commit.message}
        />
    );
};
