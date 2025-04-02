import { useEffect, useRef } from "react";

export const useIntersectionObserverRef = <T extends HTMLElement>(
  threshold: number,
  onChange: (visibility: number) => void,
) => {
  const infiniteScrollingRef = useRef<T>(null);

  useEffect(() => {
    const target = infiniteScrollingRef.current;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          onChange(entry.intersectionRatio);
        }
      },
      { threshold },
    );

    if (target) {
      observer.observe(target);
    }

    return () => {
      if (target) {
        observer.unobserve(target);
      }
    };
  }, [threshold, onChange]);

  return infiniteScrollingRef;
};
