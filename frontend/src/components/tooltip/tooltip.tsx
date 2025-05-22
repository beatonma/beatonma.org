"use client";

import {
  PointerEvent,
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
import { useClient } from "@/components/hooks/environment";
import { Nullish } from "@/types";
import { DivProps } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { classes } from "@/util/transforms";
import styles from "./tooltip.module.css";

interface TooltipProps {
  tooltip: string | Nullish;
}
export default function Tooltip(props: DivProps<TooltipProps>) {
  const { tooltip, title, ...rest } = props;
  const isClient = useClient();
  const tooltipProps = useTooltip({ tooltip });

  return (
    <div
      title={onlyIf(!isClient, tooltip) ?? title}
      {...rest}
      {...tooltipProps}
    />
  );
}

interface ParentBounds {
  left: number;
  width: number;
  bottom: number;
}

interface TooltipAttributes {
  onPointerEnter?: (event: PointerEvent) => void;
  onPointerLeave?: (event: PointerEvent) => void;
}
export const useTooltip = (props: TooltipProps): TooltipAttributes => {
  const { tooltip } = props;
  const [isVisible, setIsVisible] = useState(false);
  const id = useId();
  const parentBounds = useRef<ParentBounds>(null);

  const onPointerEnter = useCallback((ev: PointerEvent) => {
    const el = ev.currentTarget as HTMLElement;
    const bBox = el.getBoundingClientRect();
    parentBounds.current = {
      left: bBox.left,
      width: bBox.width,
      bottom: bBox.bottom,
    };
    setIsVisible(true);
  }, []);
  const onPointerLeave = useCallback((ev: PointerEvent) => {
    parentBounds.current = null;
    setIsVisible(false);
  }, []);

  useEffect(() => {
    if (isVisible) {
      const bounds = parentBounds.current;
      if (!bounds) return;

      createTooltipElement({
        parentBounds: bounds,
        id,
        tooltip,
        className:
          classes(
            "opacity-0 fixed surface-vibrant chip chip-content my-0.5",
            "text-sm text-center font-bold",
            "max-w-(--tooltip-max-width)",
          ) ?? "",
      });
    } else {
      document.getElementById(id)?.remove();
    }
  }, [isVisible, tooltip, id]);

  if (!tooltip) return {};

  return {
    onPointerEnter,
    onPointerLeave,
  };
};

const createTooltipElement = (props: {
  parentBounds: ParentBounds;
  id: string;
  tooltip: string | Nullish;
  className: string;
}) => {
  const { parentBounds, id, tooltip, className } = props;
  if (!tooltip) return null;
  const div = document.createElement("div");
  div.id = id;
  div.innerHTML = tooltip;
  div.style = "left:0;top:0;";
  div.className = className;
  document.body.append(div);

  adjustTooltipElement(div, parentBounds);
};

const adjustTooltipElement = (
  div: HTMLDivElement,
  parentBounds: ParentBounds,
) => {
  const {
    left: parentLeft,
    width: parentWidth,
    bottom: parentBottom,
  } = parentBounds;
  const { width: measuredWidth } = div.getBoundingClientRect();

  const margin = 8; // px
  let left = Math.max(margin, parentLeft + parentWidth / 2 - measuredWidth / 2);

  if (left + measuredWidth + margin > window.innerWidth) {
    left = Math.max(margin, window.innerWidth - measuredWidth - margin);
  }
  div.style = `left:${left}px;top:${parentBottom}px`;
  div.classList.replace("opacity-0", styles.tooltip);
};
