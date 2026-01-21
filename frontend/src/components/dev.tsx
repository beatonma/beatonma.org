"use client";

import { useEffect, useRef } from "react";
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

export const useDebugDetectChanges = (deps: any[], labels?: string[]) => {
  const oldDeps = useRef([...deps]);

  useEffect(() => {
    let hasChanges = false;

    const old = oldDeps.current;
    for (let i = 0; i < old.length; i++) {
      const previous = old[i];
      const current = deps[i];
      if (previous !== current) {
        console.warn(
          `Value of '${labels?.[i] || `#${i}`}' changed: ${previous} -> ${current}`,
        );
        hasChanges = true;
      }
    }

    if (hasChanges) {
      oldDeps.current = [...deps];
    }
  }, deps);
};
