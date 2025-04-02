"use client";

import { useEffect } from "react";
import Callout from "@/components/callout";
import { DivProps } from "@/types/react";

export default function Todo(props: DivProps) {
  const { children, ...rest } = props;

  useEffect(() => {
    console.log(`TODO ${children}`);
  }, []);

  return (
    <Callout level="warn" {...rest}>
      <strong className="block">TODO</strong>
      {children}
    </Callout>
  );
}
