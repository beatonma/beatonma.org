import React, { useEffect } from "react";

export const KeyboardNavigation = (props: {
    handler: (event: KeyboardEvent) => void;
}) => {
    useEffect(() => {
        window.addEventListener("keydown", props.handler);

        return () => window.removeEventListener("keydown", props.handler);
    }, [props.handler]);

    return <></>;
};
