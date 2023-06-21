import React from "react";
import { AppIcon, TextWithIcon } from "../../../components/icons";
import { Commit } from "../types";
import { pluralize } from "../plurals";
import { Dropdown } from "../../../components/dropdown";

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
                    commits.length
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
        <TextWithIcon
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
