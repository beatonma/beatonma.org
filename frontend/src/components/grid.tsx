import React, { ComponentPropsWithRef } from "react";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

const FullSpan = "col-start-1 col-span-full";

export const GridSpan = (props: ComponentPropsWithRef<"div">) => {
  return <div {...addClass(props, FullSpan)} />;
};
export const GridSpacer = (props: DivPropsNoChildren) => {
  return <div {...addClass(props, FullSpan)} />;
};
export const GridSectionHeader = (props: DivProps) => {
  return (
    <div
      {...addClass(props, FullSpan, "text-base pt-4 text-center sm:text-start")}
    />
  );
};
