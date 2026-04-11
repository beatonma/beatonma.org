"use client";

import { ReactNode, useCallback, useState } from "react";
import { Dialog } from "@/components/dialog";
import type { TupleOf } from "@/types";
import { DivProps, DivPropsNoChildren, Props } from "@/types/react";
import { addClass } from "@/util/transforms";
import { MediaCarousel } from "./media-carousel";
import { MediaThumbnail } from "./media-view";
import type { MediaFile } from "./types";

type MediaGroup<N extends number> = TupleOf<MediaFile, N>;
type OnClickThumbnailProps = { onClickMedia: (media: MediaFile) => void };
type PreviewProps<N extends number> = DivProps<{ media: MediaGroup<N> }> &
  OnClickThumbnailProps;

const NsfwStyleLarge = "nsfw-16";
const NsfwStyleSmall = "nsfw-4";

export const MediaGroupPreview = (
  props: DivPropsNoChildren<{ media: MediaFile[] }, "onClick">,
) => {
  const { media, ...rest } = addClass(props, "surface-muted overflow-hidden");
  const [fileIndex, setFileIndex] = useState<number | undefined>(undefined);

  const onClickMedia = useCallback(
    (file: MediaFile) => {
      setFileIndex(media.findIndex((it) => it.url === file.url));
    },
    [media],
  );

  if (!media.length) return null;

  const view: () => ReactNode =
    {
      1: () => (
        <PreviewOne
          media={media as MediaGroup<1>}
          onClickMedia={onClickMedia}
          {...rest}
        />
      ),
      2: () => (
        <PreviewTwo
          media={media as MediaGroup<2>}
          onClickMedia={onClickMedia}
          {...rest}
        />
      ),
      3: () => (
        <PreviewThree
          media={media as MediaGroup<3>}
          onClickMedia={onClickMedia}
          {...rest}
        />
      ),
      4: () => (
        <PreviewFour
          media={media as MediaGroup<4>}
          onClickMedia={onClickMedia}
          {...rest}
        />
      ),
    }[media.length] ??
    (() => <PreviewMany media={media} onClickMedia={onClickMedia} {...rest} />);

  return (
    <>
      {view()}

      <Dialog
        isOpen={fileIndex !== undefined}
        onClose={() => setFileIndex(undefined)}
      >
        <MediaCarousel
          media={media}
          focusIndex={fileIndex}
          className="max-h-full"
        />
      </Dialog>
    </>
  );
};

const Thumbnail = (
  props: Props<typeof MediaThumbnail> & OnClickThumbnailProps,
) => {
  const { media, onClickMedia, ...rest } = props;

  return (
    <MediaThumbnail
      media={media}
      onClick={() => onClickMedia(media)}
      {...rest}
    />
  );
};
const MiniThumbnail = (
  props: Props<
    typeof MediaThumbnail,
    OnClickThumbnailProps,
    "nsfwStyle" | "className"
  >,
) => (
  <div className="surface-scrim border-2 border-transparent rounded-md overflow-hidden">
    <Thumbnail
      {...props}
      className="w-16 aspect-square "
      nsfwStyle={NsfwStyleSmall}
    />
  </div>
);

const PreviewOne = (props: PreviewProps<1>) => {
  const { media, onClickMedia, ...rest } = props;
  return (
    <div {...rest}>
      <Thumbnail
        media={media[0]}
        onClickMedia={onClickMedia}
        video={{ autoPlay: true, loop: true }}
        className="size-full"
        nsfwStyle={NsfwStyleLarge}
      />
    </div>
  );
};

const PreviewTwo = (props: PreviewProps<2>) => {
  const { media, onClickMedia, ...rest } = props;

  const [one, two] = media;

  return (
    <div {...addClass(rest, "relative")}>
      <Thumbnail
        media={one}
        onClickMedia={onClickMedia}
        video={{ autoPlay: true, loop: true }}
        nsfwStyle={NsfwStyleLarge}
      />

      <AdditionalHint>
        <MiniThumbnail
          media={two}
          onClickMedia={onClickMedia}
          // className={SmallPreviewStyle}
          // nsfwStyle={NsfwStyleSmall}
        />
      </AdditionalHint>
    </div>
  );
};

const PreviewThree = (props: PreviewProps<3>) => {
  const { media, onClickMedia, ...rest } = props;

  const [one, two, three] = media;

  return (
    <div {...addClass(rest, "relative")}>
      <Thumbnail
        media={one}
        onClickMedia={onClickMedia}
        video={{ autoPlay: true, loop: true }}
        nsfwStyle={NsfwStyleLarge}
      />

      <AdditionalHint>
        <MiniThumbnail
          media={two}
          onClickMedia={onClickMedia}
          // className={SmallPreviewStyle}
          // nsfwStyle={NsfwStyleSmall}
        />
        <MiniThumbnail
          media={three}
          onClickMedia={onClickMedia}
          // className={SmallPreviewStyle}
          // nsfwStyle={NsfwStyleSmall}
        />
      </AdditionalHint>
    </div>
  );
};

const PreviewFour = (props: PreviewProps<4>) => {
  const { media, onClickMedia, children, ...rest } = props;

  const [one, two, three, four] = media;

  return (
    <div
      {...addClass(
        rest,
        "grid grid-cols-2 grid-rows-2 *:[.media-thumbnail]:aspect-square",
      )}
    >
      <Thumbnail
        media={one}
        onClickMedia={onClickMedia}
        nsfwStyle={NsfwStyleLarge}
      />
      <Thumbnail
        media={two}
        onClickMedia={onClickMedia}
        nsfwStyle={NsfwStyleLarge}
      />
      <Thumbnail
        media={three}
        onClickMedia={onClickMedia}
        nsfwStyle={NsfwStyleLarge}
      />
      <Thumbnail
        media={four}
        onClickMedia={onClickMedia}
        nsfwStyle={NsfwStyleLarge}
      />
      {children}
    </div>
  );
};

const PreviewMany = (
  props: DivPropsNoChildren<{ media: MediaFile[] } & OnClickThumbnailProps>,
) => {
  const { media, ...rest } = props;

  return (
    <PreviewFour
      media={media.slice(0, 4) as MediaGroup<4>}
      {...addClass(rest, "relative")}
    >
      <AdditionalHint className="text-xs surface-scrim chip chip-content pointer-events-none">
        +{media.length - 4} more
      </AdditionalHint>
    </PreviewFour>
  );
};

const AdditionalHint = (props: DivProps) => {
  const { children, ...rest } = addClass(props);
  return (
    <div
      {...addClass(
        rest,
        "absolute bottom-0 right-0 m-2 empty:hidden row gap-x-2",
      )}
    >
      {children}
    </div>
  );
};
