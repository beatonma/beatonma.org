import {
  ComponentPropsWithoutRef,
  MouseEvent,
  ReactNode,
  useContext,
} from "react";
import Icon, { AppIcon } from "@/components/icon";
import { OnClickMediaContext } from "@/components/media/context";
import { getPlaintextSummaryFromHtml } from "@/components/opengraph/text";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import { MediaFile, OnClickMedia } from "./types";

interface MediaProps {
  media: MediaFile;
}
type MediaViewProps = DivPropsNoChildren<MediaProps>;

interface ImageProps {
  image?: {
    useThumbnail?: boolean;
    fit?: MediaFile["fit"];
  };
}
type VideoOptions = Pick<
  ComponentPropsWithoutRef<"video">,
  "autoPlay" | "loop"
>;
interface VideoProps {
  video?: VideoOptions;
}

export default function MediaView(
  props: MediaViewProps & ImageProps & VideoProps,
) {
  const { image, video, ...rest } = addClass(props, "relative");

  const views: Record<MediaFile["type"], () => ReactNode> = {
    image: () => <ImageView image={image} {...rest} />,
    video: () => <VideoView video={video} {...rest} />,
    audio: () => <AudioView {...rest} />,
    text: () => <TextView {...rest} />,
    unknown: () => <BlobDownloadView {...rest} />,
  };
  return views[props.media.type]();
}
export const MediaThumbnail = (props: MediaViewProps & ImageProps) => {
  const {
    media,
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

  if (!media.thumbnail_url) {
    return <Placeholder media={media} onClick={onClick} {...rest} />;
  }

  return (
    <ImageView
      media={props.media}
      image={{ useThumbnail: true }}
      onClick={onClick}
      {...rest}
    />
  );
};

const ImageView = (props: MediaViewProps & ImageProps) => {
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

const VideoView = (props: MediaViewProps & VideoProps) => {
  const { media, video, ...rest } = props;
  return (
    <MediaWrapper {...rest}>
      <video className="size-full" src={media.url} muted controls {...video} />
    </MediaWrapper>
  );
};

const MediaWrapper = (props: DivPropsNoChildren) => {
  return <div {...addClass(props, "overflow-hidden [&>img,&>video]:m-0")} />;
};

const AudioView = (props: MediaViewProps) => {
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

const TextView = (props: MediaViewProps) => <BlobDownloadView {...props} />;

const BlobDownloadView = (props: MediaViewProps) => {
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
