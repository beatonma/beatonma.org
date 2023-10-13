import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { MediaCarousel } from "./media-carousel";
import { MediaGroupPreview } from "./media-group-preview";

export interface MediaViewerProps {
    fileUrls: string[];
}
export interface MediaViewerEntrypointProps {
    containerId: string;
}

enum MediaViewerStyle {
    Preview = "preview",
    Carousel = "carousel",
}

export const MediaViewerApp = async () => {
    document.querySelectorAll(".media-container").forEach((el: HTMLElement) => {
        const urls = el.dataset.urls.split(";").filter(it => !!it);
        const style =
            (el.dataset.mediaViewerStyle as MediaViewerStyle) ??
            MediaViewerStyle.Preview;

        if (urls.length > 0) {
            createRoot(el).render(
                <StrictMode>
                    <MediaElement
                        style={style}
                        fileUrls={urls}
                        containerId={el.id}
                    />
                </StrictMode>
            );
        }
    });
};

const MediaElement = (
    props: MediaViewerProps &
        MediaViewerEntrypointProps & { style: MediaViewerStyle }
) => {
    const { style, ...rest } = props;
    switch (style) {
        case MediaViewerStyle.Carousel:
            return <MediaCarousel {...rest} />;
        case MediaViewerStyle.Preview:
        default:
            return <MediaGroupPreview {...rest} />;
    }
};
