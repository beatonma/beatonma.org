import React, { HTMLProps } from "react";
import { IconProps, MaterialIcon } from "./icons";
import { classes } from "../props";

interface TextWithIconProps extends IconProps {
    text?: string | React.ReactNode;
    dangerousHtml?: string;
}

export const TextWithIcon = (
    props: TextWithIconProps & HTMLProps<HTMLDivElement>
) => {
    const { icon, iconClick, text, dangerousHtml, className, ...rest } = props;

    return (
        <div className={classes(className, "text-with-icon")} {...rest}>
            <MaterialIcon icon={icon} iconClick={iconClick} />

            {dangerousHtml ? (
                <span dangerouslySetInnerHTML={{ __html: dangerousHtml }} />
            ) : (
                <span>{text}</span>
            )}
        </div>
    );
};
