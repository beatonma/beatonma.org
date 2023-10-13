import React, { HTMLAttributes } from "react";

interface TooltipProps extends HTMLAttributes<any> {
    popupText: string;
}

export const Tooltip = (props: TooltipProps) => {
    const { children, popupText, title, ...rest } = props;

    return (
        <div className="tooltip" {...rest} title={popupText}>
            {children}
        </div>
    );
};
