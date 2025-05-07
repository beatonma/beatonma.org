import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const ProseClassName = "readable prose";

export default function Prose(props: DivProps) {
  return <div {...addClass(props, ProseClassName)} />;
}
