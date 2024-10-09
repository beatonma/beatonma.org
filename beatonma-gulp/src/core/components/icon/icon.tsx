import { classes } from "../../util/transform";
import React, { HTMLProps } from "react";

/**
 * Icons currently available in /static/fonts/AppIcons.woff2.
 * See /static/fonts/README.md if you need to add more.
 */
type AvailableIcon =
    | "add"
    | "alternate_email"
    | "arrow_drop_down"
    | "check"
    | "close"
    | "contrast"
    | "dashboard"
    | "done"
    | "edit"
    | "edit_note"
    | "first_page"
    | "fork_right"
    | "last_page"
    | "link"
    | "lock"
    | "mail"
    | "merge"
    | "navigate_before"
    | "navigate_next"
    | "new_releases"
    | "palette"
    | "refresh"
    | "search"
    | "shield";

export enum AppIcon {
    Add = "add",
    ArrowLeft = "navigate_before",
    ArrowRight = "navigate_next",
    ArrowDown = "arrow_drop_down",
    CheckMark = "check",
    Close = "close",
    Done = "done",
    Branch = "fork_right",
    Link = "link",
    Merge = "merge",
    Private = "lock",
    Refresh = "refresh",
    Release = "new_releases",
    Search = "search",
    Wiki = "edit_note",
}

export interface IconProps {
    icon: AvailableIcon;
    iconClick?: {
        href?: string;
        title: string;
    };
}

export const MaterialIcon = (props: HTMLProps<HTMLSpanElement> & IconProps) => {
    const { icon, iconClick, className, ...rest } = props;

    const cls = classes(className, "material-symbols-outlined");

    if (iconClick) {
        return (
            <a className={cls} href={iconClick.href} title={iconClick.title}>
                {icon}
            </a>
        );
    }

    return (
        <span className={cls} {...rest}>
            {icon}
        </span>
    );
};
