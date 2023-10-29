interface MediaQueryMap {
    "prefers-color-scheme": "light" | "dark";
    "prefers-reduced-motion": "reduce" | "no-preference";
}

export const matchMedia = <K extends keyof MediaQueryMap>(
    key: K,
    value?: MediaQueryMap[K],
): MediaQueryList => {
    const query = [key, value].map(Boolean).join(": ");
    return window.matchMedia(`(${query})`);
};

export const userPrefersColorScheme = (
    scheme: MediaQueryMap["prefers-color-scheme"],
) => matchMedia("prefers-color-scheme", scheme).matches;

export const userPrefersReducedMotion = (): boolean =>
    matchMedia("prefers-reduced-motion", "reduce").matches;
