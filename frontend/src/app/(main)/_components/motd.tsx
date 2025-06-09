import React from "react";
import Callout from "@/components/callout";
import Optional from "@/components/optional";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";

export default function GlobalMotd(
  props: DivPropsNoChildren<
    { motd: string | Nullish },
    "dangerouslySetInnerHTML"
  >,
) {
  const { motd: _motd, ...rest } = props;

  return (
    <Optional
      value={_motd}
      block={(motd) => (
        <Callout
          level="important"
          dangerouslySetInnerHTML={{ __html: motd }}
          {...rest}
        />
      )}
    />
  );
}
