export const requireElement = <T extends HTMLElement>(
    id: string,
    container: HTMLElement | Document = document
): T => {
    const element: HTMLElement =
        container instanceof Document
            ? container.getElementById(id)
            : container.querySelector(`#${id}`);

    if (!element) throw `Required element #${id} not found!`;
    return element as T;
};

/**
 * Accessor for global elements (i.e. contents of `scaffold.html`).
 */
export namespace Scaffold {
    const LoadingId = "loading";
    const ContentWrapperId = "content_wrapper";
    export const ContentId = "content";
    const ScrimId = "dialog_scrim";
    const DialogContainerId = "dialog_container";
    const LocalStyleId = "local_style";

    export const getScrim = () => requireElement(ScrimId);
    export const getDialogContainer = () => requireElement(DialogContainerId);
    export const getContent = (container: HTMLElement | Document = document) =>
        requireElement(ContentId, container);
    export const getContentWrapper = () => requireElement(ContentWrapperId);

    /**
     * Return primary content containers.
     * i.e. Child elements of <body> which make up the main UI but not those
     * used for modal content, loading bars, etc.
     */
    export const getContentContainers: () => NodeListOf<Element> = () => {
        const containers = document.querySelectorAll(
            `header, footer, #${ContentWrapperId}`
        );

        if (containers.length !== 3)
            throw `getContentContainers expects 3 items but found ${containers.length}.`;

        return containers;
    };

    export const showLoading = (visible: boolean = true) => {
        requireElement(LoadingId).dataset.active = `${visible}`;
    };

    export const importLocalStyle = (from: Element) => {
        requireElement(LocalStyleId).innerHTML = from.querySelector(
            `#${LocalStyleId}`
        ).innerHTML;
    };
}
