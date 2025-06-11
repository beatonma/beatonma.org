"use client";

import { useEffect } from "react";
import { Callout } from "@/components/callout";
import { DivProps } from "@/types/react";

export const Todo = (props: DivProps) => {
  const { children, ...rest } = props;

  useEffect(() => {
    console.log(`TODO ${children}`);
  }, [children]);

  return (
    <Callout level="warn" {...rest}>
      <strong className="block">TODO</strong>
      {children}
    </Callout>
  );
};
