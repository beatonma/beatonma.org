import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

type CalloutLevel = "tip" | "important" | "info" | "warn" | "caution";
interface CalloutProps {
  level: CalloutLevel;
}
export default function Callout(props: DivProps<CalloutProps>) {
  const { level, ...rest } = props;
  const levelStyle: Record<CalloutLevel, string> = {
    tip: "template-callout-tip",
    info: "template-callout-info",
    important: "template-callout-important",
    caution: "template-callout-caution",
    warn: "template-callout-warn",
  };

  return <div {...addClass(rest, levelStyle[level])} />;
}
