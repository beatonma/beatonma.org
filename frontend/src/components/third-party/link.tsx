import Link from "next/link";
import { Nullish } from "@/types";
import { Props, PropsExcept } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { UrlFormatStyle, formatUrl, joinNonEmpty } from "@/util/transforms";

interface ExternalLinkProps {
  follow?: boolean;
  opener?: boolean;
  referrer?: boolean;
}
export default function ExternalLink(
  props: ExternalLinkProps &
    Props<
      typeof Link,
      { href: string | Nullish; formatStyle?: UrlFormatStyle }
    >,
) {
  const {
    href,
    children,
    rel,
    follow = false,
    opener = false,
    referrer = false,
    formatStyle,
    ...rest
  } = props;
  if (!href) {
    return <span {...rest}>{children ?? formatUrl(href)}</span>;
  }

  return (
    <Link
      href={href}
      rel={joinNonEmpty(
        " ",
        rel,
        onlyIf(!follow, "nofollow"),
        onlyIf(!opener, "noopener"),
        onlyIf(!referrer, "noreferrer"),
      )}
      {...rest}
    >
      {children ?? formatUrl(href, formatStyle)}
    </Link>
  );
}
