"use client";

import type { Path, Webmention, WebmentionTester } from "@/api/types";
import { TintedButton } from "@/components/button";
import Callout from "@/components/callout";
import Webmentions from "@/components/data/webmentions";
import { parseDate } from "@/components/datetime";
import { Row } from "@/components/layout";
import Prose from "@/components/prose";
import ExternalLink from "@/components/third-party/link";
import { DivPropsNoChildren, PropsExcept } from "@/types/react";
import { plural } from "@/util/format/plurals";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

type TempMention = WebmentionTester["temporary_outgoing_mentions"][number];
type TempMentionStatus = TempMention["status"];

interface TemporaryMentionsProps {
  tempMentions: TempMention[];
}
interface WebmentionsTesterPage extends TemporaryMentionsProps {
  mentions: Webmention[];
}

export default function WebmentionsTesterPage(props: WebmentionsTesterPage) {
  const { mentions, tempMentions } = props;

  return (
    <div className="mx-auto readable space-y-16">
      <section>
        <Prose>
          <h2>Webmentions Tester</h2>

          <h3>Check that your server accepts webmentions</h3>
          <ol>
            <li>Submit a link to a page on your website.</li>
            <li>
              This page will temporarily include a link to that page, and submit
              a webmention to your server.
            </li>
          </ol>

          <noscript>
            <Callout level="warn" className="font-bold">
              Javascript is disabled: you will need to refresh the page
              manually.
            </Callout>
          </noscript>
        </Prose>

        <SubmitWebmentionForm />

        <TemporaryMentions
          tempMentions={tempMentions}
          className="readable mt-8"
        />
      </section>

      <section className="space-y-8">
        <Prose>
          <h3>Check that your server sends webmentions</h3>
          <p>Simply create a page on your site which links to this page.</p>
          <p>
            If your setup is working, your server should submit a webmention to
            this server, and you should see your mention appear below.
          </p>
        </Prose>

        <ReceivedWebmentions mentions={mentions} />
      </section>
    </div>
  );
}

const SubmitWebmentionForm = () => {
  const actionPath: Path = "/api/webmentions_tester/";

  return (
    <form action={actionPath} method="post">
      <Row className="gap-2 justify-center">
        <input
          name="url"
          type="url"
          placeholder="https://your.site/your-article/"
          autoFocus
          required
        />
        <TintedButton type="submit">Submit</TintedButton>
      </Row>
    </form>
  );
};

const TemporaryMentions = (
  props: DivPropsNoChildren<TemporaryMentionsProps>,
) => {
  const { tempMentions, ...rest } = props;

  if (!tempMentions.length) return null;

  return (
    <div
      {...addClass(
        rest,
        "flex flex-row *:shrink-0 overflow-x-auto overflow-y-hidden gap-4",
      )}
    >
      {tempMentions.map((temp) => (
        <div key={temp.submitted_at} className="card card-content surface-alt">
          <ExternalLink href={temp.url} className="prose-a" />
          <div className="text-xs text-current/90">
            Expires <TimeDescription dateTime={temp.expires_at} />
          </div>
          <TempMentionStatus status={temp.status} className="text-sm mt-2" />
        </div>
      ))}
    </div>
  );
};

const TimeDescription = (props: PropsExcept<"time", "children">) => {
  const { dateTime, ...rest } = props;
  const parsed = parseDate(dateTime);
  if (!parsed) return null;

  const now = new globalThis.Date();
  let seconds = (now.valueOf() - parsed.valueOf()) / 1000;
  const isFuture = seconds < 0;
  seconds = Math.abs(seconds);
  const hours = Math.floor(seconds / 3600);
  seconds -= hours * 3600;
  const minutes = Math.floor(seconds / 60);
  seconds -= minutes * 60;
  seconds = Math.floor(seconds);

  const formatted = [
    onlyIf(hours > 0, plural("hour", hours)),
    onlyIf(minutes > 0, plural("minute", minutes)),
    onlyIf(seconds > 0, plural("second", seconds)),
  ]
    .filter(Boolean)
    .join(" ");

  const described = isFuture ? `in ${formatted}` : `${formatted} ago`;

  return (
    <time dateTime={parsed.toISOString()} suppressHydrationWarning {...rest}>
      {described}
    </time>
  );
};

const TempMentionStatus = (
  props: DivPropsNoChildren<{ status: TempMentionStatus }>,
) => {
  const { status, ...rest } = addClass(props, "text-sm max-w-128 w-full");

  if (!status) return <div {...rest}>No status available</div>;

  return (
    <div {...rest}>
      <code>[{status.status_code}]</code> {status.message}
      <Row className="gap-2 [&>a]:text-muted [&>a]:font-mono">
        <ExternalLink href={status.source_url}>Source</ExternalLink>
        <ExternalLink href={status.target_url}>Target</ExternalLink>
        <ExternalLink href={status.endpoint}>Endpoint</ExternalLink>
      </Row>
    </div>
  );
};

const ReceivedWebmentions = (
  props: DivPropsNoChildren<{ mentions: Webmention[] }>,
) => {
  const { mentions, ...rest } = props;

  if (mentions.length) {
    return (
      <div {...rest}>
        <strong className="block mb-2">This page has been mentioned by:</strong>
        <Webmentions mentions={mentions} />
      </div>
    );
  }

  return (
    <Prose
      {...addClass(
        rest,
        "border-2 border-dashed border-muted/60 card-content rounded-md",
      )}
    >
      Nobody has mentioned this page yet :(
    </Prose>
  );
};
