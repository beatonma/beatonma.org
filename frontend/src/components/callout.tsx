import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

type CalloutLevel = "tip" | "info" | "warn";
interface CalloutProps {
  level: CalloutLevel;
}
export default function Callout(props: CalloutProps & DivProps) {
  const { level, ...rest } = props;
  const levelStyle: Record<CalloutLevel, string> = {
    tip: "surface-callout-tip",
    info: "surface-callout-info",
    warn: "surface-callout-warn",
  };

  return (
    <div
      {...addClass(rest, "card-content my-4 border-s-4", levelStyle[level])}
    />
  );
}
