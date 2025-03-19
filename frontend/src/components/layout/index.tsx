import { DivProps, DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Row = (props: DivProps) => <div {...addClass(props, "row")} />;
export const Column = (props: DivProps) => (
  <div {...addClass(props, "column")} />
);

export const Separator = (props: DivPropsNoChildren) => {
  return <div {...addClass(props, "w-0.5 h-lh bg-hover")} />;
};
