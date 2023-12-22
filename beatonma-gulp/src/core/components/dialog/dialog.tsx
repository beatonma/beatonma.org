import { useEventListener } from "../../events/event";
import { useNoScrollRef } from "../../events/scroll";
import { Scaffold } from "../../global/dom";
import React, { HTMLProps, ReactElement, useEffect, useState } from "react";
import { createRoot, Root } from "react-dom/client";

const getScrim = Scaffold.getScrim;

export namespace Scrim {
    const noop = (e: Event) => {
        e.preventDefault();
        e.stopPropagation();
    };

    export const show = () => {
        const scrim = getScrim();
        scrim.dataset.visible = "true";
        scrim.addEventListener("touchmove", noop);
        scrim.addEventListener("wheel", noop, { passive: false });
    };

    export const hide = () => {
        const scrim = getScrim();
        delete scrim.dataset.visible;
        scrim.removeEventListener("touchmove", noop);
        scrim.removeEventListener("wheel", noop);
    };
}

export namespace FullscreenDialog {
    let root: Root | null = null;

    export const mount = (node: ReactElement) => {
        if (root == null) {
            root = createRoot(Scaffold.getDialogContainer());
        }
        root?.render(node);
    };

    export const unmount = () => {
        root?.render(null);
    };
}

export const Dialog = (
    props: HTMLProps<HTMLDialogElement> & { onClose?: () => void },
) => {
    const [isOpen, setOpen] = useState(props.open);
    const { open: inheritedOpen, onClose = () => {}, ...rest } = props;
    const scrim = getScrim();

    useEffect(() => {
        setOpen(inheritedOpen);
    }, [inheritedOpen]);

    useEffect(() => {
        Scrim.show();
        disableBackground();

        return () => {
            Scrim.hide();
            enableBackground();
            onClose();
        };
    }, [isOpen]);

    // Close dialog on scrim click.
    useEventListener(scrim, ["click"], onClose);

    // Disable background scrolling
    const dialogRef = useNoScrollRef<HTMLDialogElement>();

    return <dialog ref={dialogRef} {...rest} open={isOpen} />;
};

const disableBackground = () => {
    Scaffold.getContentContainers().forEach(container => {
        container.setAttribute("aria-hidden", "true");

        getKeyboardFocusableElements(container).forEach(el => {
            el.dataset.tabIndex = `${el.tabIndex}`;
            el.dataset.disabled = "true";
            el.tabIndex = -1;
        });
    });
};

const enableBackground = () => {
    Scaffold.getContentContainers().forEach(container => {
        container.removeAttribute("aria-hidden");

        container
            .querySelectorAll("[data-disabled]")
            .forEach((el: HTMLElement) => {
                // el.tabIndex = 0;
                const restoredTabIndex = parseInt(el.dataset.tabIndex);
                el.tabIndex = isNaN(restoredTabIndex) ? 0 : restoredTabIndex;
                delete el.dataset.tabIndex;
                delete el.dataset.disabled;
            });
    });
};

/**
 * Gets keyboard-focusable elements within a specified element
 */
const getKeyboardFocusableElements = (
    element: Document | Element = document,
): HTMLElement[] => {
    const items: NodeListOf<HTMLElement> = element.querySelectorAll(
        'a[href], button, input, textarea, select, details,[tabindex]:not([tabindex="-1"])',
    );
    const itemArray: HTMLElement[] = Array(items.length);
    items.forEach((el, index) => (itemArray[index] = el));

    return itemArray.filter(
        el => !el.hasAttribute("disabled") && !el.getAttribute("aria-hidden"),
    );
};
