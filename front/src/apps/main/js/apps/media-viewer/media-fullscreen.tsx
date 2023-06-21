import React, { useEffect } from "react";
import { Dialog } from "../../components/dialog";
import { AppIcon, MaterialIcon } from "../../components/icons";
import { KeyboardNavigation } from "../../components/navigation/keyboard";
import { MediaViewerEntrypointProps } from "./index";
import { MediaCarousel, MediaCarouselProps } from "./media-carousel";

export const FullscreenMediaViewer = (
    props: MediaCarouselProps & {
        exitFullscreen: () => void;
    } & MediaViewerEntrypointProps
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

    const keyboardNavigation = (event: KeyboardEvent) => {
        switch (event.code) {
            case "Escape":
                return exitFullscreen();
        }
    };

    return (
        <Dialog
            className="media-viewer-full"
            open
            onClose={exitFullscreen}
            aria-label="Full-size media viewer"
        >
            <KeyboardNavigation handler={keyboardNavigation} />
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
