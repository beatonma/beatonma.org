import { classes } from "core/util/transform";
import React, { HTMLProps, useId } from "react";

export const Switch = (
    props: { label?: string } & HTMLProps<HTMLInputElement>,
) => {
    const { className, id = useId(), label = "", type, ...rest } = props;

    return (
        <>
            <input
                type="checkbox"
                className={classes(className, "switch")}
                id={id}
                {...rest}
            />
            <label htmlFor={id}>{label}</label>
        </>
    );
};
