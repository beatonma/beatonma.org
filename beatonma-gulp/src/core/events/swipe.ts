import { TouchEvent, useState } from "react";

const MinSwipePx = 50;

interface HorizontalSwipeHandlers {
    onSwipeLeft?: () => void;
    onSwipeRight?: () => void;
    onSwipeUp?: () => void;
    onSwipeDown?: () => void;
    preventDefault?: boolean;
    stopPropagation?: boolean;
}

interface SwipeTouchEvents {
    onTouchStart: (e: TouchEvent) => void;
    onTouchMove: (e: TouchEvent) => void;
    onTouchEnd: (e: TouchEvent) => void;
}

export const useSwipe = (config: HorizontalSwipeHandlers): SwipeTouchEvents => {
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

    const reset = () => {
        setTouchStartX(undefined);
        setTouchEndX(undefined);
    };

    const onTouchStart = (e: TouchEvent) => {
        if (preventDefault && e.cancelable) e.preventDefault();
        if (stopPropagation) e.stopPropagation();
        const touch = e.targetTouches[0];
        setTouchStartX(touch.clientX);
        setTouchStartY(touch.clientY);
    };

    const onTouchMove = (e: TouchEvent) => {
        if (preventDefault && e.cancelable) e.preventDefault();
        if (stopPropagation) e.stopPropagation();
        const touch = e.targetTouches[0];
        setTouchEndX(touch.clientX);
        setTouchEndY(touch.clientY);
    };

    const onTouchEnd = (e: TouchEvent) => {
        if (preventDefault && e.cancelable) e.preventDefault();
        if (stopPropagation) e.stopPropagation();

        const distanceX = touchEndX - touchStartX;
        const distanceY = touchEndY - touchStartY;
        const consumed =
            onHorizontalSwipe(distanceX) || onVerticalSwipe(distanceY);

        reset();
    };

    const onHorizontalSwipe = (distance: number) => {
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
    };

    const onVerticalSwipe = (distance: number) => {
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
    };

    return {
        onTouchStart,
        onTouchMove,
        onTouchEnd,
    };
};
