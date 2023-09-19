import React, { ReactNode } from "react";

interface TitleBarProps {
    title: ReactNode;
    labels?: ReactNode | ReactNode[];
    trailing?: ReactNode | ReactNode[];
    subtitle?: ReactNode | ReactNode[];
}
export const TitleBar = (props: TitleBarProps) => {
    const { title, labels, trailing, subtitle } = props;
    return (
        <div className="title-bar">
            <div className="title-bar__primary">
                <div className="title-bar__title">{title}</div>
                <div className="title-bar__labels">{labels}</div>
                <div className="title-bar__trailing">{trailing}</div>
            </div>

            <div className="title-bar__secondary">{subtitle}</div>
        </div>
    );
};
