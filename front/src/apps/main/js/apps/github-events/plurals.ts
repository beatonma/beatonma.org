const plurals: { [key: string]: [string, string] } = {
    commit: ["commit", "commits"],
    event: ["event", "events"],
    repository: ["repository", "repositories"],
};

export const pluralize = (key: string, count: number): string => {
    if (count === 1) {
        return plurals[key][0];
    } else {
        return plurals[key][1];
    }
};
