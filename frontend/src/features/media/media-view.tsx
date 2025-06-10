import { MouseEvent, ReactNode, useContext } from "react";
import Icon, { AppIcon } from "@/components/icon";
import { DivProps, DivPropsNoChildren, Props } from "@/types/react";
import { getPlaintextSummaryFromHtml } from "@/util/format/string";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import { OnClickMediaContext } from "./context";
import { MediaFile, OnClickMedia } from "./types";

type MediaProps = DivPropsNoChildren<{ media: MediaFile }>;
interface ImageProps {
  image?: {
    useThumbnail?: boolean;
    fit?: MediaFile["fit"];
  };
}
type VideoOptions = Pick<Props<"video">, "autoPlay" | "loop" | "controls"> & {
  fit?: MediaFile["fit"];
};
interface VideoProps {
  video?: VideoOptions;
}

export const MediaView = (props: MediaProps & ImageProps & VideoProps) => {
  const { image, video, ...rest } = addClass(props, "relative");

  const views: Record<MediaFile["type"], () => ReactNode> = {
    image: () => <ImageView image={image} {...rest} />,
    video: () => <VideoView video={video} {...rest} />,
    audio: () => <AudioView {...rest} />,
    text: () => <TextView {...rest} />,
    unknown: () => <BlobDownloadView {...rest} />,
  };
  return views[props.media.type]();
};
export const MediaThumbnail = (props: MediaProps & ImageProps & VideoProps) => {
  const {
    media,
    image,
    video,
    onClick: propsOnClick,
    ...rest
  } = addClass(props, "size-full");
  const onClickMedia = useContext(OnClickMediaContext);
  const onClick =
    propsOnClick ??
    onlyIf(onClickMedia, (handler: OnClickMedia) => (ev: MouseEvent) => {
      ev.preventDefault();
      ev.stopPropagation();
      handler(media);
    });

  switch (media.type) {
    case "image":
      return (
        <ImageView
          media={media}
          image={{ ...image, useThumbnail: true }}
          onClick={onClick}
          {...rest}
        />
      );
    case "video":
      return (
        <VideoView
          media={media}
          video={{ ...video, controls: false, fit: "cover" }}
          onClick={onClick}
          {...rest}
        />
      );
    default:
      return <Placeholder media={media} onClick={onClick} {...rest} />;
  }
};

const ImageView = (props: MediaProps & ImageProps) => {
  const { media, image, ...rest } = props;
  const useThumbnail = image?.useThumbnail ?? false;

  if (useThumbnail && !media.thumbnail_url) {
    return <Placeholder media={media} {...rest} />;
  }

  const src = (useThumbnail ? media.thumbnail_url : media.url) ?? "#";

  const fitStyle = {
    cover: "object-cover",
    contain: "object-contain",
  }[image?.fit ?? media.fit ?? "cover"];

  return (
    <MediaWrapper {...rest}>
      <img
        src={src}
        alt={
          media.description
            ? (getPlaintextSummaryFromHtml(media.description) ?? "")
            : ""
        }
        className={classes(fitStyle, "size-full")}
      />
    </MediaWrapper>
  );
};

const VideoView = (props: MediaProps & VideoProps) => {
  const { media, video, ...rest } = props;

  const fitStyle = {
    cover: "object-cover",
    contain: "object-contain",
  }[video?.fit ?? media.fit ?? "contain"];

  return (
    <MediaWrapper {...rest}>
      <video
        className={classes(fitStyle, "size-full")}
        src={media.url}
        muted
        controls
        {...video}
      />
    </MediaWrapper>
  );
};

const MediaWrapper = (props: DivPropsNoChildren) => {
  return <div {...addClass(props, "overflow-hidden [&>img,&>video]:m-0")} />;
};

const AudioView = (props: MediaProps) => {
  const { media, ...rest } = props;
  return (
    <div {...rest}>
      <Placeholder media={media} className="size-full">
        {onlyIf(media.name, (name) => (
          <h3 className="text-sm">{name}</h3>
        ))}
        <audio src={media.url} controls className="block mt-4" />
      </Placeholder>
    </div>
  );
};

const TextView = (props: MediaProps) => <BlobDownloadView {...props} />;

const BlobDownloadView = (props: MediaProps) => {
  const { media, ...rest } = addClass(props, "block");

  return (
    <div {...rest}>
      <a href={media.url} download>
        <Placeholder media={media} className="size-full">
          <div className="column items-center">
            {onlyIf(media.name, (name) => (
              <h3>{name}</h3>
            ))}
            <p>Click to download</p>
          </div>
        </Placeholder>
      </a>
    </div>
  );
};

const Placeholder = (props: DivProps<{ media: MediaFile }>) => {
  const { media, children, ...rest } = addClass(
    props,
    "column items-center justify-center p-4 gap-1",
  );
  const views: Record<MediaFile["type"], [AppIcon, string]> = {
    image: ["Image", "surface-media-image"],
    audio: ["Audio", "surface-media-audio"],
    text: ["Text", "surface-media-text"],
    video: ["PlayArrow", "surface-media-video"],
    unknown: ["Attachment", "surface-media-unknown"],
  };

  const [icon, className] = views[media.type];

  return (
    <div {...addClass(rest, className)}>
      <Icon
        icon={icon}
        className="max-w-1/3 max-h-1/3 w-16 h-auto aspect-square"
      />
      {children}
    </div>
  );
};
