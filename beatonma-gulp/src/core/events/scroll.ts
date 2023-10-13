import { DependencyList, useEffect, useRef } from "react";
import { useEventListener } from "./event";

const ScrollEvents = ["scroll", "mousewheel", "touchmove"];

export const useNoScroll = (
    elements: EventTarget | EventTarget[],
    deps: DependencyList = undefined,
) => useEventListener(elements, ScrollEvents, noScroll);

export const useNoScrollRef = <T extends HTMLElement>() => {
    const ref = useRef<T>();

    useEffect(() => {
        const target = ref.current;
        if (!target) return;

        const options = { passive: false };

        ScrollEvents.forEach(event => {
            target.addEventListener(event, noScroll, options);
        });

        return () => {
            ScrollEvents.forEach(event =>
                target.removeEventListener(event, noScroll),
            );
        };
    }, [ref]);

    return ref;
};

const noScroll = (ev: UIEvent) => {
    ev.preventDefault();
    ev.stopPropagation();
};
