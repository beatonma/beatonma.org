import { DependencyList, useEffect } from "react";

export const useEventListener = <T extends Event>(
    elements: EventTarget | EventTarget[],
    events: string[],
    listener: (event: T) => void,
    deps: DependencyList = undefined,
) => {
    const _elements = Array.isArray(elements) ? elements : [elements];

    return useEffect(() => {
        _elements.forEach(element =>
            events.forEach(event => {
                element.addEventListener(event, listener);
            }),
        );

        return () => {
            _elements.forEach(element =>
                events.forEach(event =>
                    element.removeEventListener(event, listener),
                ),
            );
        };
    }, deps ?? []);
};
