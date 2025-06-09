"use client";

import { HTMLAttributes, TouchEvent, useCallback, useState } from "react";

const MinSwipePx = 50;

interface SwipeHandlers {
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  onSwipeUp?: () => void;
  onSwipeDown?: () => void;
  preventDefault?: boolean;
  stopPropagation?: boolean;
}

type SwipeTouchEvents = Pick<
  HTMLAttributes<any>,
  "onTouchStart" | "onTouchMove" | "onTouchEnd"
>;

export const useSwipe = (config: SwipeHandlers): SwipeTouchEvents => {
  const [touchStartX, setTouchStartX] = useState<number>();
  const [touchEndX, setTouchEndX] = useState<number>();
  const [touchStartY, setTouchStartY] = useState<number>();
  const [touchEndY, setTouchEndY] = useState<number>();

  const {
    onSwipeLeft,
    onSwipeRight,
    onSwipeUp,
    onSwipeDown,
    preventDefault = true,
    stopPropagation = true,
  } = config;

  const reset = useCallback(() => {
    setTouchStartX(undefined);
    setTouchEndX(undefined);
  }, []);

  const onHorizontalSwipe = useCallback(
    (distance: number) => {
      if (isNaN(distance)) return false;
      if (distance > MinSwipePx && onSwipeRight) {
        onSwipeRight();
        return true;
      }
      if (distance < -MinSwipePx && onSwipeLeft) {
        onSwipeLeft();
        return true;
      }
      return false;
    },
    [onSwipeLeft, onSwipeRight],
  );

  const onVerticalSwipe = useCallback(
    (distance: number) => {
      if (isNaN(distance)) return false;
      if (distance > MinSwipePx && onSwipeUp) {
        onSwipeUp();
        return true;
      }
      if (distance < -MinSwipePx && onSwipeDown) {
        onSwipeDown();
        return true;
      }
      return false;
    },
    [onSwipeUp, onSwipeDown],
  );

  const onTouchStart = useCallback(
    (e: TouchEvent) => {
      if (preventDefault && e.cancelable) e.preventDefault();
      if (stopPropagation) e.stopPropagation();
      const touch = e.targetTouches[0];
      setTouchStartX(touch.clientX);
      setTouchStartY(touch.clientY);
    },
    [preventDefault, stopPropagation],
  );

  const onTouchMove = useCallback(
    (e: TouchEvent) => {
      if (preventDefault && e.cancelable) e.preventDefault();
      if (stopPropagation) e.stopPropagation();
      const touch = e.targetTouches[0];
      setTouchEndX(touch.clientX);
      setTouchEndY(touch.clientY);
    },
    [preventDefault, stopPropagation],
  );

  const onTouchEnd = (e: TouchEvent) => {
    if (preventDefault && e.cancelable) e.preventDefault();
    if (stopPropagation) e.stopPropagation();

    if (
      touchEndX === undefined ||
      touchStartX === undefined ||
      touchEndY === undefined ||
      touchStartY === undefined
    ) {
      return;
    }

    const distanceX = touchEndX - touchStartX;
    const distanceY = touchEndY - touchStartY;
    const consumed = onHorizontalSwipe(distanceX) || onVerticalSwipe(distanceY);

    reset();
  };

  return {
    onTouchStart,
    onTouchMove,
    onTouchEnd,
  };
};
