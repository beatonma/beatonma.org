"use client";

import { useCallback, useMemo, useState } from "react";
import { Button } from "@/components/button";
import { CheckBox } from "@/components/form";
import { useFadeIn } from "@/components/hooks/animation";
import { useClient } from "@/components/hooks/environment";
import { useSwipe, useWheel } from "@/components/hooks/inputs";
import { AppIcon } from "@/components/icon";
import { Row } from "@/components/layout";
import { DivPropsNoChildren, PropsWithRef, StateSetter } from "@/types/react";
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
  const [showNsfw, setShowNsfw] = useState(false);

  const focussedMedia = useMemo(() => media[focusIndex], [focusIndex, media]);
  const mediaLength = useMemo(() => media.length, [media]);
  const hasNsfw: boolean = useMemo(
    () => media.find((it) => it.is_nsfw) !== undefined,
    [media],
  );

  const navigatePrevious = useCallback(() => {
    setFocusIndex((prev) => {
      const target = prev - 1;
      return target < 0 ? mediaLength - 1 : target;
    });
  }, [mediaLength]);
  const navigateNext = useCallback(() => {
    setFocusIndex((prev) => {
      const target = prev + 1;
      return target >= mediaLength ? 0 : target;
    });
  }, [mediaLength]);

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
        media={focussedMedia}
        navigatePrevious={mediaLength > 1 ? navigatePrevious : undefined}
        navigateNext={mediaLength > 1 ? navigateNext : undefined}
        nsfwClass={showNsfw ? "" : "nsfw-16"}
        {...swipeNavigation}
        {...wheelNavigation}
      />

      <ContentControls
        hasNsfw={hasNsfw}
        showNsfw={showNsfw}
        setShowNsfw={setShowNsfw}
        className="px-edge"
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
          <CarouselItem key={item.url} media={item} nsfwClass="nsfw-noscript" />
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
      nsfwClass: string;
      navigatePrevious?: (() => void) | undefined;
      navigateNext?: (() => void) | undefined;
    },
    "children"
  >,
) => {
  const { ref, media, navigatePrevious, navigateNext, nsfwClass, ...rest } =
    props;
  const animation = useFadeIn(media);

  return (
    <figure
      ref={ref}
      {...addClass(
        rest,
        "relative card grid grid-rows-[1fr_auto] grid-cols-1 justify-center bg-neutral-900/50 overflow-hidden group",
        animation,
      )}
    >
      <div className="relative overflow-hidden [--button-margin:--spacing(2)]">
        <MediaView
          media={media}
          image={{ fit: "contain" }}
          video={{ autoPlay: true, loop: true }}
          className="min-w-64 self-center size-full"
          nsfwStyle={nsfwClass}
        />

        {onlyIf(navigatePrevious, (onClick) => (
          <ControlButton
            icon="ChevronLeft"
            onClick={onClick}
            className="absolute bottom-(--button-margin) left-(--button-margin)"
          />
        ))}

        {onlyIf(navigateNext, (onClick) => (
          <ControlButton
            icon="ChevronRight"
            onClick={onClick}
            className="absolute bottom-(--button-margin) right-(--button-margin)"
          />
        ))}
      </div>

      {onlyIf(media.description, (description) => (
        <figcaption className=" self-justify-center p-2">
          <div
            className="text-md readable max-h-[3lh] overflow-y-auto scrollbar mx-auto border-2 border-muted p-4 rounded-md"
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
  const { media, focusIndex, onClickIndex, ...rest } = props;

  if (media.length < 2) return null;

  return (
    <Row scrollable {...addClass(rest, "gap-4 px-edge")}>
      {media.map((item, index) => (
        <div
          key={item.url}
          className={classes(
            "rounded-md w-32 border-2 overflow-hidden bg-input",
            index === focusIndex ? "border-vibrant" : "border-transparent",
          )}
        >
          <MediaThumbnail
            className="aspect-square"
            media={item}
            onClick={() => onClickIndex(index)}
            nsfwStyle="blur-[4px] grayscale-70"
          />
        </div>
      ))}
    </Row>
  );
};

const ContentControls = (
  props: DivPropsNoChildren<{
    hasNsfw: boolean;
    showNsfw: boolean;
    setShowNsfw: StateSetter<boolean>;
  }>,
) => {
  const { hasNsfw, showNsfw, setShowNsfw, ...rest } = props;
  if (!hasNsfw) return null;

  return (
    <div {...rest}>
      <CheckBox
        isChecked={showNsfw}
        setChecked={setShowNsfw}
        label="Show nsfw"
        className="w-fit chip chip-content surface-muted"
      />
    </div>
  );
};
