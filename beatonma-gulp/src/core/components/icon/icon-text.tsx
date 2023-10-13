import { classes } from "../../util/transform";
import { IconProps, MaterialIcon } from "./icon";
import React, { HTMLProps } from "react";

interface IconWithTextProps extends IconProps {
    text?: string | React.ReactNode;
    dangerousHtml?: string;
}

export const IconWithText = (
    props: IconWithTextProps & HTMLProps<HTMLDivElement>,
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
