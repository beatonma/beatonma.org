import React, { ReactNode } from "react";

interface TitleBarProps {
    title: ReactNode;
    image?: ReactNode | ReactNode[];
    labels?: ReactNode | ReactNode[];
    trailing?: ReactNode | ReactNode[];
    subtitle?: ReactNode | ReactNode[];
}
export const TitleBar = (props: TitleBarProps) => {
    const { title, image, labels, trailing, subtitle } = props;
    return (
        <div className="title-bar">
            <div className="title-bar__inline-image">{image}</div>

            <div className="title-bar__text-wrapper">
                <div className="title-bar__primary">
                    <div className="title-bar__title">{title}</div>
                    <div className="title-bar__labels">{labels}</div>
                    <div className="title-bar__trailing">{trailing}</div>
                </div>
            </div>

            <div className="title-bar__secondary">{subtitle}</div>
        </div>
    );
};
