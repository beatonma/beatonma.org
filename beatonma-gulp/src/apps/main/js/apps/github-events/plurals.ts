const Plurals = {
    commit: ["commit", "commits"],
    event: ["event", "events"],
    repository: ["repository", "repositories"],
};

export type PluralKey = keyof typeof Plurals;
export const pluralize = (key: PluralKey, count: number): string => {
    if (count === 1) {
        return Plurals[key][0];
    } else {
        return Plurals[key][1];
    }
};
