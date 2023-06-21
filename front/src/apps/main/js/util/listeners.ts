import { DependencyList, useEffect, useRef } from "react";
import { requireElement } from "../dom";

const ScrollEvents = ["scroll", "mousewheel", "touchmove"];

export const useEventListener = <T extends Event>(
    elements: (HTMLElement | Document | Window)[],
    events: string[],
    listener: (event: T) => void,
    deps: DependencyList = undefined
) =>
    useEffect(() => {
        elements.forEach(element =>
            events.forEach(event => {
                element.addEventListener(event, listener);
            })
        );

        return () => {
            elements.forEach(element =>
                events.forEach(event =>
                    element.removeEventListener(event, listener)
                )
            );
        };
    }, deps ?? []);

export const useTextEventListener = (
    elementId: string,
    onEvent: (value: string) => void,
    eventName: string = "change",
    deps: DependencyList = undefined
) => {
    const element = requireElement(elementId);

    const listener = (event: Event) => {
        const target = event.target;
        if (
            target instanceof HTMLInputElement ||
            target instanceof HTMLTextAreaElement
        ) {
            onEvent(target.value);
        }
    };

    return useEventListener([element], [eventName], listener, deps);
};

export const useNoScroll = (
    element: (Document | HTMLElement | Window)[],
    deps: DependencyList = undefined
) => useEventListener(element ?? [document], ScrollEvents, Listeners.noScroll);

export const useNoScrollRef = <T extends HTMLElement>() => {
    const ref = useRef<T>();

    useEffect(() => {
        const target = ref.current;
        if (!target) return;

        const options = { passive: false };

        ScrollEvents.forEach(event => {
            target.addEventListener(event, Listeners.noScroll, options);
        });

        return () => {
            ScrollEvents.forEach(event =>
                target.removeEventListener(event, Listeners.noScroll)
            );
        };
    }, [ref]);

    return ref;
};

export namespace Listeners {
    export const noScroll = (ev: UIEvent) => {
        ev.preventDefault();
        ev.stopPropagation();
    };
}
