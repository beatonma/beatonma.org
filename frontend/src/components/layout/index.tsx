import { DivProps, DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

export const scrollableRow =
  "row overflow-x-auto overflow-y-hidden *:shrink-0 ";
export const Row = ({
  scrollable,
  ...rest
}: DivProps & { scrollable?: boolean }) => (
  <div {...addClass(rest, scrollable ? scrollableRow : "row")} />
);

export const Separator = (props: DivPropsNoChildren) => {
  return <div {...addClass(props, "w-0.5 h-lh bg-hover")} />;
};
