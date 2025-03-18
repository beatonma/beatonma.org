import Image from "next/image";
import { ReactNode, useContext } from "react";
import { MediaFile, OnClickMediaContext } from "@/components/media/common";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

interface ImageProps {
  image?: {
    useThumbnail?: boolean;
    fit?: MediaFile["fit"];
  };
}

interface MediaViewProps {
  media: MediaFile;
  className?: string;
}

export default function MediaView(
  props: { media: MediaFile } & ImageProps & Omit<DivPropsNoChildren, "onLoad">,
) {
  const { image, ...rest } = props;

  const views: Record<MediaFile["type"], () => ReactNode> = {
    image: () => <ImageView image={image} {...rest} />,
    video: () => <VideoView {...rest} />,
    audio: () => <AudioView {...rest} />,
    text: () => <TextView {...rest} />,
    unknown: () => null,
  };
  return views[props.media.type]();
}
export const MediaThumbnail = (
  props: { media: MediaFile } & ImageProps & Omit<DivPropsNoChildren, "onLoad">,
) => {
  const { media, ...rest } = addClass(props, "size-full");
  const onClickMedia = useContext(OnClickMediaContext);

  return (
    <ImageView
      media={props.media}
      image={{ useThumbnail: true }}
      onClick={() => onClickMedia?.(props.media)}
      {...rest}
    />
  );
};

const ImageView = (props: MediaViewProps & ImageProps) => {
  const { media, image, ...rest } = props;
  const useThumbnail = image?.useThumbnail ?? false;
  if (useThumbnail && !media.thumbnail_url) {
    return <div {...rest}>No thumbnail placeholder {media.url}</div>;
  }

  const src = (useThumbnail ? media.thumbnail_url : media.url) ?? "#";

  const fitStyle = {
    cover: "object-cover",
    contain: "object-contain",
  }[image?.fit ?? media.fit ?? "cover"];

  return (
    <Image
      src={src}
      alt={media.description ?? ""}
      width={1440}
      height={1440}
      {...addClass(rest, fitStyle)}
    />
  );
};

const VideoView = ({ media, ...rest }: MediaViewProps) => {
  return <video src={media.url} muted controls {...rest} />;
};

const AudioView = ({ media, ...rest }: MediaViewProps) => {
  return <audio src={media.url} {...rest} />;
};

const TextView = ({ media, ...rest }: MediaViewProps) => {
  return <div {...rest}>TODO: TextView {media.url}</div>;
};
