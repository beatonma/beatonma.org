import { useEffect, useRef } from "react";

export const useOnScrollIntoViewRef = <T extends HTMLElement = HTMLDivElement>(
  threshold: number,
  onScrollIntoView: () => void,
) => {
  const elementRef = useRef<T>(null);

  useEffect(() => {
    const target = elementRef.current;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            onScrollIntoView();
          }
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
  }, [threshold, onScrollIntoView]);

  return elementRef;
};
