"use client";

import { useCallback, useState } from "react";
import { Button } from "@/components/button";
import { useFadeIn } from "@/components/hooks/animation";
import { useClient } from "@/components/hooks/environment";
import { useSwipe, useWheel } from "@/components/hooks/inputs";
import { AppIcon } from "@/components/icon";
import { Row } from "@/components/layout";
import { Optional } from "@/components/optional";
import { DivPropsNoChildren, PropsWithRef } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import { MediaThumbnail, MediaView } from "./media-view";
import type { MediaFile } from "./types";

interface MediaCarouselProps {
  media: MediaFile[];
  focusIndex?: number;
}

export const MediaCarousel = (
  props: DivPropsNoChildren<MediaCarouselProps>,
) => {
  const { media } = props;
  const isClient = useClient();

  if (!media.length) return null;
  return isClient ? (
    <ControlledCarousel {...props} />
  ) : (
    <NoscriptCarousel {...props} />
  );
};

const ControlledCarousel = (props: DivPropsNoChildren<MediaCarouselProps>) => {
  const { media, focusIndex: defaultFocusIndex, ...rest } = props;
  const [focusIndex, setFocusIndex] = useState(defaultFocusIndex ?? 0);

  const navigatePrevious = useCallback(() => {
    setFocusIndex((prev) => {
      const target = prev - 1;
      return target < 0 ? media.length - 1 : target;
    });
  }, [media]);
  const navigateNext = useCallback(() => {
    setFocusIndex((prev) => {
      const target = prev + 1;
      return target >= media.length ? 0 : target;
    });
  }, [media]);

  const swipeNavigation = useSwipe({
    onSwipeLeft: navigateNext,
    onSwipeRight: navigatePrevious,
    preventDefault: false,
  });
  const wheelNavigation = useWheel({
    onWheelLeft: navigatePrevious,
    onWheelRight: navigateNext,
  });

  return (
    <div {...addClass(rest, "grid grid-cols-1 grid-rows-[1fr_auto] gap-4")}>
      <CarouselItem
        media={media[focusIndex]}
        navigatePrevious={media.length > 1 ? navigatePrevious : undefined}
        navigateNext={media.length > 1 ? navigateNext : undefined}
        {...swipeNavigation}
        {...wheelNavigation}
      />

      <CarouselThumbnails
        media={media}
        focusIndex={focusIndex}
        onClickIndex={setFocusIndex}
      />
    </div>
  );
};

const NoscriptCarousel = (props: DivPropsNoChildren<MediaCarouselProps>) => {
  const { media, focusIndex, ...rest } = props;

  return (
    <noscript>
      <div
        {...addClass(
          rest,
          "grid grid-flow-col grid-rows-1 auto-cols-max gap-4 max-w-full relative",
          "overflow-x-auto scrollbar",
        )}
      >
        {media.map((item, index) => (
          <CarouselItem key={item.url} media={item} />
        ))}
      </div>
    </noscript>
  );
};

const CarouselItem = (
  props: PropsWithRef<
    "figure",
    {
      media: MediaFile;
      navigatePrevious?: (() => void) | undefined;
      navigateNext?: (() => void) | undefined;
    },
    "children"
  >,
) => {
  const { ref, media, navigatePrevious, navigateNext, ...rest } = props;
  const animation = useFadeIn(media);

  return (
    <figure
      ref={ref}
      {...addClass(
        rest,
        "card grid grid-rows-[1fr_auto] grid-cols-1 justify-center bg-neutral-900/50 overflow-hidden",
        animation,
      )}
    >
      <div className="relative overflow-hidden [--button-margin:--spacing(2)]">
        <MediaView
          media={media}
          image={{ fit: "contain" }}
          video={{ autoPlay: true, loop: true }}
          className="min-w-64 self-center size-full"
        />

        <Optional
          value={navigatePrevious}
          block={(onClick) => (
            <ControlButton
              icon="ChevronLeft"
              onClick={onClick}
              className="absolute bottom-(--button-margin) left-(--button-margin)"
            />
          )}
        />
        <Optional
          value={navigateNext}
          block={(onClick) => (
            <ControlButton
              icon="ChevronRight"
              onClick={onClick}
              className="absolute bottom-(--button-margin) right-(--button-margin)"
            />
          )}
        />
      </div>

      {onlyIf(media.description, (description) => (
        <figcaption className="surface p-4 self-justify-center">
          <div
            className="text-md readable max-h-[3lh] overflow-y-auto scrollbar mx-auto"
            dangerouslySetInnerHTML={{ __html: description }}
          />
        </figcaption>
      ))}
    </figure>
  );
};

const ControlButton = (
  props: DivPropsNoChildren<{ icon: AppIcon; onClick: () => void }>,
) => {
  const { icon, onClick, ...rest } = props;
  return (
    <div {...rest}>
      <Button
        icon={icon}
        onClick={onClick}
        colors="hover-surface-scrim"
        className="text-2xl border-1 border-current/20"
      />
    </div>
  );
};

interface CarouselThumbnailsProps {
  media: MediaFile[];
  focusIndex: number;
  onClickIndex: (index: number) => void;
}
const CarouselThumbnails = (
  props: DivPropsNoChildren<CarouselThumbnailsProps>,
) => {
  const { media, focusIndex, onClickIndex, ...rest } = addClass(
    props,
    "gap-4 px-edge",
  );

  if (media.length < 2) return null;

  return (
    <Row scrollable {...rest}>
      {media.map((item, index) => (
        <MediaThumbnail
          className={classes(
            "aspect-square rounded-md w-32 border-2",
            index === focusIndex ? "border-vibrant" : "border-transparent",
          )}
          key={item.url}
          media={item}
          onClick={() => onClickIndex(index)}
        />
      ))}
    </Row>
  );
};
