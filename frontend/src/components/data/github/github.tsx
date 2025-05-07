import { InlineLink } from "@/components/button";
import {
  GithubRecent,
  GroupedEventPayloads,
  GroupedPrivateEvents,
  GroupedPublicEvents,
  isPrivateGroup,
} from "@/components/data/github/types";
import { groupEvents } from "@/components/data/github/util";
import { Date } from "@/components/datetime";
import { AppIcon } from "@/components/icon";
import { Row } from "@/components/layout";
import ExternalLink from "@/components/third-party/link";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { testId } from "@/util";
import { plural } from "@/util/plurals";
import { addClass } from "@/util/transforms";

const TestTarget = {
  GithubActivity: "github_activity",
};

export default function GithubActivity(
  props: { activity: GithubRecent } & DivPropsNoChildren,
) {
  const { activity, ...rest } = props;

  const grouped = groupEvents(activity.events);

  return (
    <div
      {...addClass(rest, "@container px-edge")}
      {...testId(TestTarget.GithubActivity)}
    >
      <h3>
        <ExternalLink
          href={`https://github.com/${process.env.NEXT_PUBLIC_GITHUB_USERNAME}`}
        >{`github/${process.env.NEXT_PUBLIC_GITHUB_USERNAME}`}</ExternalLink>
      </h3>
      <div className="space-y-2">
        {grouped.map((group) => {
          if (isPrivateGroup(group)) {
            return <PrivateEvents key={group.timestamp} group={group} />;
          } else {
            return (
              <PublicEvents
                key={group.timestamp}
                group={group}
                className="hover-extra-background before:-inset-1"
              />
            );
          }
        })}
      </div>
    </div>
  );
}

const EventHeadline = (props: { timestamp: number } & DivProps) => {
  const { timestamp, children, ...rest } = props;
  return (
    <Row key={timestamp} {...addClass(rest, "gap-2 justify-between")}>
      {children}
      <Date className="text-sm @max-sm:hidden" date={timestamp} />
    </Row>
  );
};

const PrivateEvents = (
  props: { group: GroupedPrivateEvents } & DivPropsNoChildren,
) => {
  const { group, ...rest } = props;

  return (
    <EventHeadline
      timestamp={group.timestamp}
      {...addClass(rest, "text-current/80")}
    >
      {plural("change", group.changeCount)} in{" "}
      {plural(
        "repository",
        group.repositoryCount,
        (repos) =>
          `${group.repositoryCount === 1 ? "a " : group.repositoryCount} private ${repos}`,
      )}
    </EventHeadline>
  );
};

const PublicEvents = (
  props: { group: GroupedPublicEvents } & DivPropsNoChildren,
) => {
  const { group, ...rest } = props;
  const { create, release, issue, wiki, push, pullRequest } = group.events;
  return (
    <div key={group.timestamp} {...rest}>
      <EventHeadline timestamp={group.timestamp}>
        <strong>
          <ExternalLink href={group.repository.url}>
            {group.repository.name}
          </ExternalLink>
        </strong>
      </EventHeadline>

      <Row className="gap-3 *:shrink-0 overflow-x-auto overflow-y-hidden text-current/80">
        <CreateEvents payload={create} />
        <PushEvents payload={push} />
        <PullRequestEvents payload={pullRequest} />
        <ReleaseEvents payload={release} />
        <IssueEvents payload={issue} />
        <WikiEvents payload={wiki} />
      </Row>
    </div>
  );
};

const CreateEvents = (props: { payload: GroupedEventPayloads["create"] }) => {
  const { payload } = props;

  if (!payload.length) return null;

  const icons: Record<string, AppIcon> = {
    tag: "Tag",
    branch: "GitBranch",
  };

  return (
    <>
      {payload.map((item) => (
        <InlineLink
          href={null}
          key={`${item.ref_type}-${item.ref}`}
          icon={icons[item.ref_type ?? ""]}
          tooltip={`New ${item.ref_type}`}
        >
          {item.ref}
        </InlineLink>
      ))}
    </>
  );
};

const PushEvents = (props: { payload: GroupedEventPayloads["push"] }) => {
  const { payload } = props;

  if (!payload.length) return null;

  const allCommitsUrl = /^(https:\/\/github.com\/.*\/commits\/).*/.exec(
    payload[0].url,
  )?.[1];

  return (
    <InlineLink icon="GitCommit" href={allCommitsUrl} tooltip="Commits">
      {payload.length}
    </InlineLink>
  );
};

const ReleaseEvents = (props: { payload: GroupedEventPayloads["release"] }) => {
  const { payload } = props;

  if (!payload.length) return null;

  return (
    <>
      {payload.map((item) => (
        <InlineLink
          key={item.url}
          href={item.url}
          icon="GitRelease"
          tooltip="Release"
        >
          {item.name}
        </InlineLink>
      ))}
    </>
  );
};

const PullRequestEvents = (props: {
  payload: GroupedEventPayloads["pullRequest"];
}) => {
  const { payload } = props;

  if (!payload.length) return null;

  return (
    <>
      {payload.map((item) => (
        <InlineLink
          key={item.number}
          icon="GitMerge"
          href={item.url}
          tooltip="Merged pull request"
        >
          {item.number}
        </InlineLink>
      ))}
    </>
  );
};

const IssueEvents = (props: { payload: GroupedEventPayloads["issue"] }) => {
  const { payload } = props;

  if (!payload.length) return null;
  return (
    <>
      {payload.map((item) => (
        <InlineLink
          key={item.number}
          icon="GitBugfix"
          href={item.url}
          tooltip="Closed issue"
        >
          {item.number}
        </InlineLink>
      ))}
    </>
  );
};

const WikiEvents = (props: { payload: GroupedEventPayloads["wiki"] }) => {
  const { payload } = props;

  if (!payload.length) return null;

  const wikiUrl = /^(https:\/\/github.com\/[^/]+\/[^/]+\/wiki\/).*/.exec(
    payload[0].url,
  )?.[1];

  return (
    <InlineLink icon="GitWiki" href={wikiUrl} tooltip="Wiki edits">
      {payload.length}
    </InlineLink>
  );
};
