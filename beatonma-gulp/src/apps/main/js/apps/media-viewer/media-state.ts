import {
    setSearchParams,
    deleteSearchParams,
    searchParams,
} from "../../util/location";

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
        focusIndex: number
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
