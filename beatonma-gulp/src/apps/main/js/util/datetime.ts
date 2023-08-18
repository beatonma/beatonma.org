export const formatDateISO = (date: string | Date): string =>
    new Date(date).toISOString().slice(0, 10);

export const formatDate = (
    date: string | Date,
    options: Intl.DateTimeFormatOptions = {
        day: "2-digit",
        month: "long",
        year: "numeric",
    },
    separator: string = " "
) => {
    const _date = new Date(date);
    const now = new Date();

    _date.setHours(0, 0, 0, 0);
    now.setHours(0, 0, 0, 0);

    if (
        _date.getMonth() === now.getMonth() &&
        _date.getDate() === now.getDate() &&
        _date.getFullYear() === now.getFullYear()
    ) {
        return "Today";
    }

    now.setDate(now.getDate() - 1);
    if (
        _date.getMonth() === now.getMonth() &&
        _date.getDate() === now.getDate() &&
        _date.getFullYear() === now.getFullYear()
    ) {
        return "Yesterday";
    }

    if (_date.getFullYear() === now.getFullYear()) {
        delete options["year"];
    }

    const day = _date.toLocaleDateString("default", { day: options.day });
    const month = _date.toLocaleDateString("default", { month: options.month });
    const year = options.year
        ? _date.toLocaleDateString("default", { year: options.year })
        : null;

    return [day, month, year].filter(Boolean).join(separator);
};

export const formatTimeDelta = (
    totalSeconds: number,
    options = { verbose: false }
) => {
    const hours = Math.floor(totalSeconds / 3600);
    let remaining = totalSeconds % 3600;
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;

    const verbose = options.verbose;
    const hoursLabel = verbose ? " hours" : "h";
    const minutesLabel = verbose ? " minutes" : "min";
    const secondsLabel = verbose ? " seconds" : "sec";

    if (hours) {
        if (minutes === 0) return `${hours}${hoursLabel}`;
        return `${hours}${hoursLabel} ${minutes}${minutesLabel}`;
    }

    if (minutes) {
        if (minutes > 15) return `~${minutes}${minutesLabel}`;
        return `${minutes}${minutesLabel} ${seconds}${secondsLabel}`;
    }

    return `${seconds}${secondsLabel}`;
};
