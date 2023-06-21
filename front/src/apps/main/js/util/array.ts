export const shuffle = <T>(array: T[]): T[] => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
};

export const groupBy = <T>(array: T[], predicate: (value: T) => any) => {
    const groups: Record<any, T[]> = {};

    array.forEach(item => {
        const key = predicate(item);
        if (!(key in groups)) {
            groups[key] = [];
        }
        groups[key].push(item);
    });

    return groups;
};
