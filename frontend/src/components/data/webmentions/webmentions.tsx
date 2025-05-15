import { type Webmention } from "@/api/types";
import { InlineLink } from "@/components/button";
import Optional from "@/components/optional";
import ExternalLink from "@/components/third-party/link";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, formatUrl } from "@/util/transforms";

interface WebmentionsProps {
  mentions: Webmention[];
}

export default function Webmentions(
  props: WebmentionsProps & DivPropsNoChildren,
) {
  const { mentions, ...rest } = addClass(
    props,
    "grid grid-cols-1 md:grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-4 items-start",
  );

  return (
    <div {...rest}>
      {mentions.map((mention) => (
        <Webmention key={mention.source_url} mention={mention} />
      ))}
    </div>
  );
}

interface WebmentionProps {
  mention: Webmention;
}
const Webmention = (props: WebmentionProps & DivPropsNoChildren) => {
  const { mention, ...rest } = addClass(
    props,
    "p-2 surface-alt md:rounded-md",
    "grid grid-cols-[auto_1fr] gap-y-2",
    onlyIf(props.mention.quote, "col-start-1 md:col-span-2"),
    "[&_a]:hover:underline",
  );

  return (
    <div {...rest}>
      <HCardAvatar hcard={mention.hcard} className="col-start-1 me-2 size-12" />
      <div className="col-start-2">
        <HCardLinkedName hcard={mention.hcard} />
        <InlineLink href={mention.source_url} />
      </div>

      <Optional
        value={mention.quote}
        block={(quote) => (
          <blockquote className="col-span-full border-l-2 border-vibrant pl-2">
            {quote}
          </blockquote>
        )}
      />
    </div>
  );
};

interface HCardProps {
  hcard: Webmention["hcard"];
}
const HCardAvatar = (props: HCardProps & DivPropsNoChildren) => {
  const { hcard, ...rest } = addClass(
    props,
    "rounded-md overflow-hidden surface-muted",
    "aspect-square place-content-center text-center font-bold",
    "border-2 border-current/20 select-none",
  );
  return (
    <div {...rest}>
      {hcard?.avatar ? (
        <img
          src={hcard.avatar}
          alt={undefined}
          className="size-full overflow-hidden"
        />
      ) : (
        (hcard?.name || formatUrl(hcard?.homepage) || "?")?.[0]
      )}
    </div>
  );
};

const HCardLinkedName = (props: HCardProps & DivPropsNoChildren) => {
  const { hcard, ...rest } = addClass(props, "font-bold text-current/70");
  if (!hcard || (!hcard.name && !hcard.homepage)) return null;
  return (
    <div {...rest}>
      {hcard.homepage ? (
        <ExternalLink href={hcard.homepage}>
          {hcard.name || formatUrl(hcard.homepage)}
        </ExternalLink>
      ) : (
        hcard.name
      )}
    </div>
  );
};
