import React from "react";
import Callout from "@/components/callout";
import Optional from "@/components/optional";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";

export default function GlobalMotd(
  props: { motd: string | Nullish } & Omit<
    DivPropsNoChildren,
    "dangerouslySetInnerHMTL"
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
