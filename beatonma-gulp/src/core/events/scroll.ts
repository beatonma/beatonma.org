import { useEffect, useRef } from "react";

const ScrollEvents = ["scroll", "mousewheel", "touchmove"];

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
};
