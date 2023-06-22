import React, { HTMLAttributes } from "react";
import { classes } from "./props";

export const Row = (props: HTMLAttributes<HTMLDivElement>) => (
    <div className={classes(props.className, "row")}>{props.children}</div>
);
