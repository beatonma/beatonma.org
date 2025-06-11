import { PropsWithRef } from "@/types/react";
import { addClass } from "@/util/transforms";

const FullSpan = "col-start-1 col-span-full";

export const GridSpan = (props: PropsWithRef) => (
  <div {...addClass(props, FullSpan)} />
);
