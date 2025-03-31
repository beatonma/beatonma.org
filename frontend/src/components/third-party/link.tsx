import { ComponentPropsWithoutRef } from "react";
import { onlyIf } from "@/util/optional";
import { joinNonEmpty } from "@/util/transforms";

interface ExternalLinkProps {
  follow?: boolean;
  opener?: boolean;
  referrer?: boolean;
}
export default function ExternalLink(
  props: ExternalLinkProps & ComponentPropsWithoutRef<"a">,
) {
  const {
    rel,
    follow = false,
    opener = false,
    referrer = false,
    ...rest
  } = props;
  return (
    <a
      rel={joinNonEmpty(
        " ",
        rel,
        onlyIf(!follow, "nofollow"),
        onlyIf(!opener, "noopener"),
        onlyIf(!referrer, "noreferrer"),
      )}
      {...rest}
    />
  );
}
