import React from "react";
import DangerousHtml from "@/components/html";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

export default function GlobalHCard(
  props: { hcard: string | Nullish } & DivPropsNoChildren,
) {
  const { hcard, ...rest } = props;
  return <DangerousHtml html={hcard} {...addClass(rest, "h-card")} />;
}
