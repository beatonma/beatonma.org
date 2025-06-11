import { ReactNode } from "react";
import { AppIcon, Icon } from "@/components/icon";
import { DivProps, Props } from "@/types/react";
import { getPlaintextSummaryFromHtml } from "@/util/format/string";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import { MediaFile } from "./types";

export type MediaElementProps = Props<"div"> & Props<"img"> & Props<"video">;
type MediaProps = MediaElementProps & { media: MediaFile };
type Fit = MediaFile["fit"];

interface ImageProps {
  image?: {
    fit?: Fit;
  };
}
type VideoOptions = Pick<Props<"video">, "autoPlay" | "loop" | "controls"> & {
  fit?: Fit;
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
  const { media, image, video, ...rest } = addClass(props);

  switch (media.type) {
    case "image":
      return (
        <ImageView
          media={{ ...media, url: media.thumbnail_url ?? media.url }}
          image={{ ...image }}
          {...rest}
        />
      );
    case "video":
      return (
        <VideoView
          media={media}
          video={{ ...video, controls: false, fit: "cover" }}
          {...rest}
        />
      );
    default:
      return <Placeholder media={media} {...rest} />;
  }
};

const ImageView = (props: MediaProps & ImageProps) => {
  const { media, image, className, ...rest } = props;
  const fitStyle = chooseFitStyle(image?.fit, media?.fit, "cover");

  return (
    <img
      src={media.url}
      alt={
        media.description
          ? (getPlaintextSummaryFromHtml(media.description) ?? "")
          : ""
      }
      className={classes(className, fitStyle)}
      {...rest}
    />
  );
};

const VideoView = (props: MediaProps & VideoProps) => {
  const { media, video, className, ...rest } = props;
  const fitStyle = chooseFitStyle(video?.fit, media?.fit, "contain");

  return (
    <video
      className={classes(className, fitStyle)}
      src={media.url}
      muted
      controls
      {...video}
      {...rest}
    />
  );
};

const AudioView = (props: MediaProps) => {
  const { media, ...rest } = props;
  return (
    <div {...rest}>
      <Placeholder media={media} className="size-full">
        {onlyIf(media.name, (name) => (
          <h3 className="text-sm line-clamp-1">{name}</h3>
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
      <Placeholder download media={media} className="size-full">
        {onlyIf(media.name, (name) => (
          <h3 className="line-clamp-1">{name}</h3>
        ))}
        <p>Click to download</p>
      </Placeholder>
    </div>
  );
};

const Placeholder = (
  props: DivProps<{ media: MediaFile; download?: boolean }>,
) => {
  const { media, download = false, children, ...rest } = props;
  const views: Record<MediaFile["type"], [AppIcon, string]> = {
    image: ["Image", "surface-media-image"],
    audio: ["Audio", "surface-media-audio"],
    text: ["Text", "surface-media-text"],
    video: ["PlayArrow", "surface-media-video"],
    unknown: ["Attachment", "surface-media-unknown"],
  };

  const [icon, className] = views[media.type];
  const contentProps = {
    className:
      "max-w-full max-h-full mx-auto column items-center justify-center gap-1 aspect-square",
    children: (
      <>
        <Icon
          icon={icon}
          className="max-w-16 max-h-16 min-w-4 min-h-4 w-1/3 h-auto"
        />
        {children}
      </>
    ),
  };

  return (
    <div {...addClass(rest, className, "p-2")}>
      {download ? (
        <a download href={media.url} {...contentProps} />
      ) : (
        <div {...contentProps} />
      )}
    </div>
  );
};

const chooseFitStyle = (
  primary: Fit | undefined,
  secondary: Fit | undefined,
  fallback: Fit,
): string | undefined => {
  const key = primary ?? secondary ?? fallback;
  if (key) {
    return {
      cover: "object-cover",
      contain: "object-contain",
    }[key];
  }
};
