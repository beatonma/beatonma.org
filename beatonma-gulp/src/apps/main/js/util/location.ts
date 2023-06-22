export const searchParams = () => new URLSearchParams(window.location.search);

export const setSearchParams = (params: Record<string, any>) => {
    const search = searchParams();

    Object.entries(params).forEach(([key, value]) => {
        search.set(key, value);
    });

    applySearchParams(search);
};

export const deleteSearchParams = (...names: string[]) => {
    const search = searchParams();

    names.forEach(key => search.delete(key));
    applySearchParams(search);
};

const applySearchParams = (params: URLSearchParams): void => {
    window.history.replaceState({}, "", `${location.pathname}?${params}`);
};
