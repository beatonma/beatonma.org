import { useEffect, useRef } from "react";
import { MediaFile } from "@/components/media/common";
import MediaView from "@/components/media/media-view";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

interface MediaCarouselProps {
  media: MediaFile[];
  focusIndex?: number;
}
export default function MediaCarousel(
  props: MediaCarouselProps & DivPropsNoChildren,
) {
  const { media, focusIndex, ...rest } = props;
  return (
    <div
      {...addClass(
        rest,
        "grid grid-flow-col grid-rows-1 auto-cols-max sm:px-4 gap-4 overflow-x-auto scrollbar py-4 max-w-full relative",
      )}
    >
      {media.map((item, index) => (
        <CarouselItem
          key={item.url}
          media={item}
          className="[--max-height:80vh] max-h-(--max-height) max-w-(--max-width)"
          isFocussed={index === focusIndex}
        />
      ))}
    </div>
  );
}

const CarouselItem = (
  props: { media: MediaFile; isFocussed: boolean } & DivPropsNoChildren,
) => {
  const { media, isFocussed, ...rest } = props;
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let timerId: ReturnType<typeof setTimeout>;
    if (ref.current && isFocussed) {
      timerId = setTimeout(() => {
        ref.current?.scrollIntoView({ inline: "center" });
      }, 100);
    }

    return () => {
      if (timerId) {
        clearTimeout(timerId);
      }
    };
  }, [isFocussed]);

  return (
    <figure
      ref={onlyIf(isFocussed, ref)}
      {...addClass(
        rest,
        "card grid grid-rows-[1fr_auto] grid-cols-1 justify-center w-fit bg-neutral-900/50",
      )}
    >
      <MediaView
        media={media}
        image={{ fit: "contain" }}
        className="max-h-full min-w-64 self-center size-full"
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
