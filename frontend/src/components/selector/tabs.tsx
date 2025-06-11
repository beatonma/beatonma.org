"use client";

import underlineStyles from "@/components/css/hover-underline.module.css";
import { addClass, classes } from "@/util/transforms";
import type { SelectorDivProps } from "./types";

export const TabBar = (props: SelectorDivProps) => {
  const { selected, items, onSelect, ...rest } = props;

  return (
    <div
      {...addClass(
        rest,
        "flex flex-row gap-2 *:shrink-0 overflow-x-auto overflow-y-hidden",
      )}
    >
      {items.map((it) => (
        <div
          key={it.key}
          data-selected={selected.key === it.key}
          className={classes(
            `transition-colors [--padding:--spacing(1)] px-2 py-(--padding) [--underline-offset:var(--padding)] ${underlineStyles.hoverUnderline}`,
            selected.key === it.key
              ? "hover cursor-default font-medium"
              : `hover opacity-80 cursor-pointer hover:bg-hover hover:opacity-100 [--underline-color:var(--muted)]`,
          )}
          onClick={() => onSelect(it)}
        >
          {it.display}
        </div>
      ))}
    </div>
  );
};
