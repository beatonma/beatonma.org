"use client";

import { useState } from "react";
import Dialog from "@/components/dialog";
import MediaCarousel from "@/components/media/media-carousel";
import { MediaThumbnail } from "@/components/media/media-view";
import { TupleOf } from "@/types";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import { type MediaFile, OnClickMediaContext } from "./common";

type MediaGroup<N extends number> = TupleOf<MediaFile, N>;

const PreviewMiniStyle = "aspect-square rounded-md border-2 border-current";

export default function MediaPreview(
  props: { media: MediaFile[] } & DivPropsNoChildren,
) {
  const { media, ...rest } = addClass(props, "size-full @container");
  const [fileIndex, setFileIndex] = useState<number | undefined>(undefined);

  const onClickMedia = (file: MediaFile) => {
    setFileIndex(media.findIndex((it) => it.url === file.url));
  };

  const view = {
    0: () => null,
    1: () => <PreviewOne media={media[0]} {...rest} />,
    2: () => <PreviewTwo media={media as MediaGroup<2>} {...rest} />,
    3: () => <PreviewThree media={media as MediaGroup<3>} {...rest} />,
    4: () => <PreviewFour media={media as MediaGroup<4>} {...rest} />,
  }[media.length];

  return (
    <OnClickMediaContext.Provider value={onClickMedia}>
      {view?.() ?? <PreviewMany media={media} {...rest} />}

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
    </OnClickMediaContext.Provider>
  );
}

const MiniThumbnailOverlay = (props: DivProps) => {
  return (
    <div
      {...addClass(props, "absolute column gap-2 bottom-0 right-0 m-2 w-1/6")}
    />
  );
};

const PreviewOne = (
  props: { media: MediaFile } & Omit<DivPropsNoChildren, "onClick">,
) => {
  const { media, ...rest } = props;
  return (
    <MediaThumbnail media={media} {...addClass(rest, "overflow-hidden")} />
  );
};

const PreviewTwo = (props: { media: MediaGroup<2> } & DivPropsNoChildren) => {
  const { media, ...rest } = addClass(props, "relative overflow-hidden");

  const [one, two] = media;

  return (
    <div {...rest}>
      <MediaThumbnail media={one} className="overflow-hidden" />

      <MiniThumbnailOverlay>
        <MediaThumbnail media={two} className={`${PreviewMiniStyle}`} />
      </MiniThumbnailOverlay>
    </div>
  );
};

const PreviewThree = (props: { media: MediaGroup<3> } & DivPropsNoChildren) => {
  const { media, ...rest } = addClass(props, "relative overflow-hidden");

  const [one, two, three] = media;

  return (
    <div {...rest}>
      <MediaThumbnail media={one} className="overflow-hidden" />

      <MiniThumbnailOverlay>
        <MediaThumbnail media={two} className={PreviewMiniStyle} />
        <MediaThumbnail media={three} className={PreviewMiniStyle} />
      </MiniThumbnailOverlay>
    </div>
  );
};

const PreviewFour = (props: { media: MediaGroup<4> } & DivProps) => {
  const { media, children, ...rest } = addClass(
    props,
    "grid grid-cols-2 grid-rows-2 *:aspect-square",
  );

  const [one, two, three, four] = media;

  return (
    <div {...rest}>
      <MediaThumbnail media={one} />
      <MediaThumbnail media={two} />
      <MediaThumbnail media={three} />
      <MediaThumbnail media={four} />
      {children}
    </div>
  );
};

const PreviewMany = (props: { media: MediaFile[] } & DivPropsNoChildren) => {
  const { media, ...rest } = addClass(props, "relative");

  return (
    <PreviewFour media={media.slice(0, 4) as MediaGroup<4>} {...rest}>
      <div className="absolute surface-scrim chip chip-content bottom-0 right-0 m-2">
        +{media.length - 4}
      </div>
    </PreviewFour>
  );
};
