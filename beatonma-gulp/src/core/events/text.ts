import { requireElement } from "../global/dom";
import { useEventListener } from "./event";
import { DependencyList } from "react";

export const useTextEventListener = (
    elementId: string,
    onEvent: (value: string) => void,
    eventName: string = "change",
    deps: DependencyList = undefined,
) => {
    const element = requireElement(elementId);

    const listener = (event: KeyboardEvent) => {
        const target = event.target;
        if (
            target instanceof HTMLInputElement ||
            target instanceof HTMLTextAreaElement
        ) {
            switch (event.key) {
                case "Escape":
                    target.blur();
                    break;
                default:
                    onEvent(target.value);
            }
        }
    };

    return useEventListener([element], [eventName], listener, deps);
};
