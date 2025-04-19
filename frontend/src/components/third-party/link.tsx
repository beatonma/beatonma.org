import Link from "next/link";
import { PropsExcept } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { formatUrl, joinNonEmpty } from "@/util/transforms";

interface ExternalLinkProps {
  follow?: boolean;
  opener?: boolean;
  referrer?: boolean;
}
export default function ExternalLink(
  props: ExternalLinkProps &
    PropsExcept<typeof Link, "href"> & { href: string },
) {
  const {
    href,
    children,
    rel,
    follow = false,
    opener = false,
    referrer = false,
    ...rest
  } = props;
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
      {children ?? formatUrl(href)}
    </Link>
  );
}
