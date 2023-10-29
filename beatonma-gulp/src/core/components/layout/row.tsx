import { classes } from "../../util/transform";
import React, { HTMLAttributes } from "react";

export const Row = (props: HTMLAttributes<HTMLDivElement>) => {
    const { className, children, ...rest } = props;
    return (
        <div className={classes(className, "row")} {...rest}>
            {children}
        </div>
    );
};
