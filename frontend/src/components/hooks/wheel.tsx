"use client";

import {
  HTMLAttributes,
  WheelEvent,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

const MinWheelDelta = 1;
type WheelEvents = Pick<HTMLAttributes<any>, "onWheel">;

interface WheelHandlers {
  onWheelLeft?: () => void;
  onWheelRight?: () => void;
  onWheelUp?: () => void;
  onWheelDown?: () => void;
  cooldownMillis?: number; // Cooldown between event firings
}
export default function useWheel(config: WheelHandlers): WheelEvents {
  const {
    onWheelLeft,
    onWheelRight,
    onWheelUp,
    onWheelDown,
    cooldownMillis = 200,
  } = config;
  const isOnCooldown = useRef(false);
  const [cooldown, setOnCooldown] = useState(false);

  useEffect(() => {
    let timerId: ReturnType<typeof setTimeout>;
    if (cooldown) {
      timerId = setTimeout(() => {
        setOnCooldown(false);
        isOnCooldown.current = false;
      }, cooldownMillis);
    }
    return () => {
      clearTimeout(timerId);
    };
  }, [cooldown, cooldownMillis]);

  const onWheel = useCallback(
    (ev: WheelEvent) => {
      if (isOnCooldown.current) return;
      let consumed = false;
      if (ev.deltaX > MinWheelDelta && onWheelRight) {
        onWheelRight();
        consumed = true;
      } else if (ev.deltaX < -MinWheelDelta && onWheelLeft) {
        onWheelLeft();
        consumed = true;
      }

      if (ev.deltaY > MinWheelDelta && onWheelUp) {
        onWheelUp();
        consumed = true;
      } else if (ev.deltaY < -MinWheelDelta && onWheelDown) {
        onWheelDown();
        consumed = true;
      }

      if (consumed) {
        isOnCooldown.current = true;
        setOnCooldown(true);
      }
    },
    [onWheelLeft, onWheelRight, onWheelUp, onWheelDown],
  );

  return {
    onWheel: onWheel,
  };
}
