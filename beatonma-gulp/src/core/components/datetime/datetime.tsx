import { formatDate, formatDateISO } from "../../components/datetime/format";
import React, { HTMLProps } from "react";

export enum DateTimeFormat {
    DateISO,
    Normal,
}

const DateTimeFormatter = {
    [DateTimeFormat.DateISO]: formatDateISO,
    [DateTimeFormat.Normal]: formatDate,
};

interface DateTimeFormatProps {
    format?: DateTimeFormat;
}

export const Time = (
    props: HTMLProps<HTMLTimeElement> & DateTimeFormatProps,
) => {
    const { dateTime, title, format = DateTimeFormat.Normal, ...rest } = props;

    if (!dateTime) return null;

    const displayText = DateTimeFormatter[format](dateTime);
    const titleText =
        format === DateTimeFormat.Normal
            ? undefined // Don't show title if same as displayText
            : DateTimeFormatter[DateTimeFormat.Normal](dateTime);

    return (
        <time title={title ?? titleText} dateTime={dateTime} {...rest}>
            {displayText}
        </time>
    );
};
