import { useEffect } from "react";

interface WindowEvent<K extends keyof WindowEventMap> {
    type: K;
    handler: (this: Window, ev: WindowEventMap[K]) => void;
}

export const useWindowEventListener = <K extends keyof WindowEventMap>(
    props: WindowEvent<K>,
) => {
    const { type, handler } = props;
    return useEffect(() => {
        window.addEventListener(type, handler);

        return () => window.removeEventListener(type, handler);
    }, [props.handler]);
};

export const useKeyDownWindowEvent = (
    handler: (event: KeyboardEvent) => void,
) => useWindowEventListener({ type: "keydown", handler: handler });
