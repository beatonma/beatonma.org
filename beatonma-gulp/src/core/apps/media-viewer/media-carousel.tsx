import { AppIcon, MaterialIcon } from "../../components/icon";
import { useSwipe } from "../../events/swipe";
import { useKeyDownWindowEvent } from "../../events/window";
import { MediaViewerEntrypointProps, MediaViewerProps } from "./index";
import { Media } from "./media";
import { MediaState } from "./media-state";
import React, { useEffect, useRef, useState } from "react";

export interface MediaCarouselProps extends MediaViewerProps {
    focusIndex?: number;
}

export const MediaCarousel = (
    props: MediaCarouselProps & MediaViewerProps & MediaViewerEntrypointProps,
) => {
    const {
        containerId,
        focusIndex: defaultFocusIndex = MediaState.restoreFocusIndex(
            containerId,
        ) ?? 0,
        fileUrls,
    } = props;
    const [focussedIndex, setFocussedIndex] = useState(defaultFocusIndex);
    const [focussed, setFocussed] = useState(fileUrls?.[focussedIndex]);

    useEffect(() => {
        setFocussed(fileUrls[focussedIndex]);
        if (focussedIndex == null) {
            MediaState.defocus();
        } else {
            MediaState.setFocus(containerId, focussedIndex);
        }
    }, [focussedIndex]);

    useEffect(() => {
        return MediaState.defocus;
    }, []);

    const navigatePrevious = () => {
        const target = focussedIndex - 1;
        setFocussedIndex(target < 0 ? fileUrls.length - 1 : target);
    };

    const navigateNext = () => {
        const target = focussedIndex + 1;
        setFocussedIndex(target >= fileUrls.length ? 0 : target);
    };

    useKeyDownWindowEvent((event: KeyboardEvent) => {
        switch (event.code) {
            case "ArrowLeft":
                return navigatePrevious();
            case "ArrowRight":
                return navigateNext();
        }
    });

    const swipeNavigation = useSwipe({
        onSwipeLeft: navigateNext,
        onSwipeRight: navigatePrevious,
        preventDefault: false,
    });

    return (
        <div className="media-carousel">
            <div
                className="media-carousel--focussed"
                data-item-count={fileUrls.length}
            >
                <div
                    className="media-carousel--focussed-primary"
                    {...swipeNavigation}
                >
                    {fileUrls.map(url => (
                        <Media
                            src={url}
                            key={url}
                            showControls={url === focussed}
                            allowAutoplay={url === focussed}
                            data-visible={url === focussed}
                        />
                    ))}
                </div>

                <NavigationButtons
                    fileCount={fileUrls.length}
                    onClickPrevious={navigatePrevious}
                    onClickNext={navigateNext}
                />
            </div>

            <Items
                fileUrls={fileUrls}
                focussedIndex={focussedIndex}
                onClick={index => setFocussedIndex(index)}
            />
        </div>
    );
};

const NavigationButtons = (props: {
    fileCount: number;
    onClickPrevious: () => void;
    onClickNext: () => void;
}) => {
    const { fileCount, onClickPrevious, onClickNext } = props;

    if (fileCount < 2) return null;

    return (
        <>
            <div className="media-carousel--navigation">
                <button onClick={onClickPrevious}>
                    <MaterialIcon icon={AppIcon.ArrowLeft} />
                </button>
                <button onClick={onClickNext}>
                    <MaterialIcon icon={AppIcon.ArrowRight} />
                </button>
            </div>
        </>
    );
};

const Items = (
    props: MediaViewerProps & {
        onClick: (n: number) => void;
        focussedIndex: number;
    },
) => {
    const { fileUrls, focussedIndex, onClick } = props;

    if (fileUrls.length < 2) return null;

    return (
        <div className="media-carousel--items">
            {fileUrls.map((url, index) => {
                const ref = useRef<HTMLImageElement | HTMLVideoElement>();
                const isSelected = index === focussedIndex;

                useEffect(() => {
                    if (isSelected) {
                        scrollToItem(ref.current);
                    }
                }, [isSelected]);

                return (
                    <Media
                        ref={ref}
                        src={url}
                        key={url}
                        onClick={() => onClick(index)}
                        allowAutoplay={false}
                        showControls={false}
                        data-selected={isSelected}
                    />
                );
            })}
        </div>
    );
};

const scrollToItem = (item: HTMLElement) => {
    if (!item) throw "Reference not set";

    const container = item.parentElement;

    container.scrollLeft =
        item.offsetLeft - item.offsetWidth / 2 - container.offsetLeft;
};
