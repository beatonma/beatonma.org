import { FullscreenDialog } from "../../components/dialog";
import { MediaViewerEntrypointProps, MediaViewerProps } from "./index";
import { Media } from "./media";
import { FullscreenMediaViewer } from "./media-fullscreen";
import { MediaState } from "./media-state";
import React, { useEffect, useState } from "react";

export const MediaGroupPreview = (
    props: MediaViewerProps & MediaViewerEntrypointProps,
) => {
    const { fileUrls, containerId } = props;
    const [focusIndex, setFocusIndex] = useState<number | null>(
        MediaState.restoreFocusIndex(containerId),
    );

    useEffect(() => {
        if (focusIndex !== null) {
            FullscreenDialog.mount(
                <FullscreenMediaViewer
                    containerId={containerId}
                    focusIndex={focusIndex}
                    exitFullscreen={() => setFocusIndex(null)}
                    fileUrls={fileUrls}
                />,
            );
            MediaState.setFocus(containerId, focusIndex);
        } else {
            MediaState.defocus(containerId, () =>
                setTimeout(FullscreenDialog.unmount),
            );
        }
    }, [focusIndex]);

    return (
        <div className="media-group-preview" data-item-count={fileUrls.length}>
            {fileUrls.map((file, index) => (
                <div className="media-griditem" key={file}>
                    <Media src={file} onClick={() => setFocusIndex(index)} />
                </div>
            ))}
        </div>
    );
};
