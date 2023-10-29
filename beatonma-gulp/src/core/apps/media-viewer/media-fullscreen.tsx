import { Dialog } from "../../components/dialog";
import { AppIcon, MaterialIcon } from "../../components/icon";
import { useKeyDownWindowEvent } from "../../events/window";
import { MediaViewerEntrypointProps } from "./index";
import { MediaCarousel, MediaCarouselProps } from "./media-carousel";
import React, { useEffect } from "react";

export const FullscreenMediaViewer = (
    props: MediaCarouselProps & {
        exitFullscreen: () => void;
    } & MediaViewerEntrypointProps,
) => {
    const { exitFullscreen, focusIndex, ...rest } = props;

    useEffect(() => {
        if (focusIndex != null) {
            document.body.style.overflow = "hidden";
        }

        return () => {
            document.body.style.overflow = "auto";
        };
    }, [focusIndex]);

    if (focusIndex == null) return null;

    useKeyDownWindowEvent((event: KeyboardEvent) => {
        switch (event.code) {
            case "Escape":
                return exitFullscreen();
        }
    });

    return (
        <Dialog
            className="media-viewer-full"
            open
            onClose={exitFullscreen}
            aria-label="Full-size media viewer"
        >
            <MediaCarousel focusIndex={focusIndex} {...rest} />
            <CloseDialogButton onClick={exitFullscreen} />
        </Dialog>
    );
};

const CloseDialogButton = (props: { onClick: () => void }) => {
    return (
        <button className="close-dialog" onClick={props.onClick}>
            <MaterialIcon icon={AppIcon.Close} />
        </button>
    );
};
