import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Row = (props: DivProps) => <div {...addClass(props, "row")} />;
export const Column = (props: DivProps) => (
  <div {...addClass(props, "column")} />
);
