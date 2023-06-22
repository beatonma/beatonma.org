import React, { HTMLAttributes } from "react";
import { AppIcon, TextWithIcon } from "../../../components/icons";
import { Url } from "../types/common";
import { classes } from "../../../components/props";

interface BadgeProps extends HTMLAttributes<any> {
    url: Url;
    icon: AppIcon;
    issue?: number;
    text?: string;
    title: string;
}

export const Badge = (props: BadgeProps) => {
    const { url, title, icon, issue, text, className, ...rest } = props;

    return (
        <a href={url} title={title}>
            <TextWithIcon
                icon={icon}
                text={`${issue ?? text}`}
                className={classes(className, "badge")}
                {...rest}
            />
        </a>
    );
};
