import { AppIcon, IconWithText } from "../../../components/icon";
import { classes } from "../../../util/transform";
import { Url } from "../types/common";
import React, { HTMLAttributes } from "react";

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
            <IconWithText
                icon={icon}
                text={`${issue ?? text}`}
                className={classes(className, "github-badge")}
                {...rest}
            />
        </a>
    );
};
