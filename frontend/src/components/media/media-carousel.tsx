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
        "row sm:px-4 gap-4 overflow-x-auto scrollbar items-end py-4",
      )}
    >
      {media.map((item, index) => (
        <CarouselItem
          key={item.url}
          media={item}
          className="max-h-[80vh] shrink-0"
          isFocussed={index === focusIndex}
        />
      ))}
    </div>
  );
}

const CarouselItem = (
  props: { media: MediaFile; isFocussed: boolean } & DivPropsNoChildren,
) => {
  const { media, isFocussed, ...rest } = addClass(
    props,
    "card surface items-center column max-w-full gap-4 xl:flex-row xl:items-start p-2",
  );
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  return (
    <div ref={onlyIf(isFocussed, ref)} {...rest}>
      <MediaView
        media={media}
        image={{ fit: "contain" }}
        className="max-h-[80vh] sm:rounded-md xl:rounded-r-none"
      />
      {onlyIf(media.description, (description) => (
        <div
          className="font-bold text-lg readable text-center px-edge overflow-auto shrink-0
        xl:max-w-[300px] xl:text-left max-xl:max-h-[5em] "
        >
          {description}
        </div>
      ))}
    </div>
  );
};
