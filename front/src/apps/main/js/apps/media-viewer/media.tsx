import React, { ForwardedRef, forwardRef, HTMLProps } from "react";
import { userPrefersReducedMotion } from "../../util/accessibility";

const IMAGE_FILE_TYPES: string[] = [
    "apng",
    "avif",
    "gif",
    "jpg",
    "jpeg",
    "png",
    "svg",
    "webp",
];
const VIDEO_FILE_TYPES: string[] = ["mp4", "webm"];

interface MediaProps {
    src: string;
    onClick?: () => void;
    allowAutoplay?: boolean;
    showControls?: boolean;
}

export const Media = forwardRef(
    (
        props: MediaProps &
            (HTMLProps<HTMLImageElement> | HTMLProps<HTMLVideoElement>),
        ref: ForwardedRef<HTMLElement>
    ) => {
        const { src, onClick, showControls, allowAutoplay, ...rest } = props;

        if (isImage(src)) {
            return (
                <Image
                    src={src}
                    onClick={onClick}
                    {...rest}
                    ref={ref as ForwardedRef<HTMLImageElement>}
                />
            );
        }
        if (isVideo(src)) {
            return (
                <Video
                    src={src}
                    onClick={onClick}
                    showControls={showControls}
                    allowAutoplay={allowAutoplay}
                    {...rest}
                    ref={ref as ForwardedRef<HTMLVideoElement>}
                />
            );
        }

        console.warn(`Unhandled media: '${src}'`);

        return null;
    }
);
const Image = forwardRef(
    (props: MediaProps, ref: ForwardedRef<HTMLImageElement>) => {
        const { src, onClick, ...rest } = props;
        return (
            <img
                className="media"
                src={src}
                alt=""
                loading="lazy"
                onClick={ev => {
                    ev.preventDefault();
                    ev.stopPropagation();
                    onClick?.();
                }}
                ref={ref}
                {...rest}
            />
        );
    }
);
const Video = forwardRef(
    (props: MediaProps, ref: ForwardedRef<HTMLVideoElement>) => {
        const {
            src,
            onClick,
            allowAutoplay = true,
            showControls = false,
            ...rest
        } = props;
        const autoplay = allowAutoplay && !userPrefersReducedMotion();

        return (
            <video
                className="media"
                src={src}
                muted={autoplay}
                autoPlay={autoplay}
                controls={showControls}
                loop={autoplay}
                onClick={ev => {
                    ev.preventDefault();
                    ev.stopPropagation();
                    onClick?.();
                }}
                ref={ref}
                {...rest}
            />
        );
    }
);

const fileExtension = (url: string) => url.match(/\.(\w+)$/)?.[1];
const isImage = (url: string) => IMAGE_FILE_TYPES.includes(fileExtension(url));
const isVideo = (url: string) => VIDEO_FILE_TYPES.includes(fileExtension(url));
