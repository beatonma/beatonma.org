import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const ProseClassName = "readable prose";

export const Prose = (props: DivProps) => (
  <div {...addClass(props, ProseClassName)} />
);
