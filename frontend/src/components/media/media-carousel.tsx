"use client";

import { ComponentPropsWithRef, useCallback, useState } from "react";
import { Button } from "@/components/button";
import { useFadeIn } from "@/components/hooks/animation";
import { useClient } from "@/components/hooks/environment";
import useSwipe from "@/components/hooks/swipe";
import useWheel from "@/components/hooks/wheel";
import { Row } from "@/components/layout";
import { MediaFile } from "@/components/media/common";
import MediaView, { MediaThumbnail } from "@/components/media/media-view";
import Optional from "@/components/optional";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";

interface MediaCarouselProps {
  media: MediaFile[];
  focusIndex?: number;
}
export default function MediaCarousel(
  props: MediaCarouselProps & DivPropsNoChildren,
) {
  const { media } = props;
  const isClient = useClient();

  if (!media.length) return null;
  return isClient ? (
    <ControlledCarousel {...props} />
  ) : (
    <NoscriptCarousel {...props} />
  );
}

const ControlledCarousel = (props: MediaCarouselProps & DivPropsNoChildren) => {
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
      <div
        className="relative overflow-hidden max-h-full"
        {...swipeNavigation}
        {...wheelNavigation}
      >
        <CarouselItem media={media[focusIndex]} />
        <Optional
          value={media.length > 1}
          block={() => (
            <CarouselControls
              navigatePrevious={navigatePrevious}
              navigateNext={navigateNext}
            />
          )}
        />
      </div>

      <CarouselThumbnails
        media={media}
        focusIndex={focusIndex}
        onClickIndex={setFocusIndex}
      />
    </div>
  );
};

const NoscriptCarousel = (props: MediaCarouselProps & DivPropsNoChildren) => {
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
  props: { media: MediaFile } & Omit<
    ComponentPropsWithRef<"figure">,
    "children"
  >,
) => {
  const { ref, media, ...rest } = props;
  const animation = useFadeIn(media);

  return (
    <figure
      ref={ref}
      {...addClass(
        rest,
        "card grid grid-rows-[1fr_auto] grid-cols-1 justify-center bg-neutral-900/50 overflow-hidden size-full",
        animation,
      )}
    >
      <MediaView
        media={media}
        image={{ fit: "contain" }}
        video={{ autoPlay: true, loop: true }}
        className="max-h-full min-w-64 self-center size-full overflow-hidden"
      />

      {onlyIf(media.description, (description) => (
        <figcaption className="surface p-4 self-justify-center">
          <p className="font-bold text-lg readable max-h-[3lh] overflow-y-auto scrollbar mx-auto">
            {description}
          </p>
        </figcaption>
      ))}
    </figure>
  );
};

interface CarouselControlsProps {
  navigateNext: () => void;
  navigatePrevious: () => void;
}
const CarouselControls = (props: CarouselControlsProps) => {
  const { navigateNext, navigatePrevious } = props;

  const buttonColors = "hover-surface-scrim";
  const buttonClass = "text-2xl border-1 border-current/20";

  return (
    <>
      <div className="absolute bottom-0 start-0 m-2">
        <Button
          icon="ChevronLeft"
          onClick={navigatePrevious}
          colors={buttonColors}
          className={buttonClass}
        />
      </div>
      <div className="absolute bottom-0 end-0 m-2">
        <Button
          icon="ChevronRight"
          onClick={navigateNext}
          colors={buttonColors}
          className={buttonClass}
        />
      </div>
    </>
  );
};

interface CarouselThumbnailsProps {
  media: MediaFile[];
  focusIndex: number;
  onClickIndex: (index: number) => void;
}
const CarouselThumbnails = (
  props: CarouselThumbnailsProps & DivPropsNoChildren,
) => {
  const { media, focusIndex, onClickIndex, ...rest } = addClass(
    props,
    "gap-4 *:shrink-0 overflow-x-auto px-edge",
  );

  if (media.length < 2) return null;

  return (
    <Row {...rest}>
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
