export namespace MediaState {
    const ParamID = "media_group";
    const ParamFocussed = "media_index";

    export const restoreFocusIndex = (containerId: string): number | null => {
        const search = searchParams();
        if (search.get(ParamID) === containerId) {
            const urlFocussedIndex = parseInt(search.get(ParamFocussed));
            if (!isNaN(urlFocussedIndex)) {
                return urlFocussedIndex;
            }
        }
        return null;
    };

    export const setFocus = (
        containerId: string | null,
        focusIndex: number,
    ) => {
        setSearchParams({
            [ParamID]: containerId,
            [ParamFocussed]: focusIndex,
        });
    };

    export const setFocusIndex = (focusIndex: number) => {
        setSearchParams({ [ParamFocussed]: focusIndex });
    };

    export const defocus = (containerId?: string, onDefocus?: () => void) => {
        if (
            containerId === undefined ||
            containerId === searchParams().get(ParamID)
        ) {
            deleteSearchParams(ParamID, ParamFocussed);
            onDefocus?.();
        }
    };
}

const searchParams = () => new URLSearchParams(window.location.search);

const setSearchParams = (params: Record<string, any>) => {
    const search = searchParams();

    Object.entries(params).forEach(([key, value]) => {
        search.set(key, value);
    });

    applySearchParams(search);
};

const deleteSearchParams = (...names: string[]) => {
    const search = searchParams();

    names.forEach(key => search.delete(key));
    applySearchParams(search);
};

const applySearchParams = (params: URLSearchParams): void => {
    window.history.replaceState({}, "", `${location.pathname}?${params}`);
};
