import { ReactNode, useContext } from "react";
import Icon, { AppIcon } from "@/components/icon";
import { MediaFile, OnClickMediaContext } from "@/components/media/common";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

interface MediaViewProps {
  media: MediaFile;
  className?: string;
  onClick?: () => void;
}

interface ImageProps {
  image?: {
    useThumbnail?: boolean;
    fit?: MediaFile["fit"];
  };
}

export default function MediaView(
  props: MediaViewProps &
    ImageProps &
    Omit<DivPropsNoChildren, keyof MediaViewProps>,
) {
  const { image, ...rest } = addClass(props, "relative");

  const views: Record<MediaFile["type"], () => ReactNode> = {
    image: () => <ImageView image={image} {...rest} />,
    video: () => <VideoView {...rest} />,
    audio: () => <AudioView {...rest} />,
    text: () => <TextView {...rest} />,
    unknown: () => <BlobDownloadView {...rest} />,
  };
  return views[props.media.type]();
}
export const MediaThumbnail = (
  props: MediaViewProps &
    ImageProps &
    Omit<DivPropsNoChildren, keyof MediaViewProps>,
) => {
  const { media, ...rest } = addClass(props, "size-full");
  const onClickMedia = useContext(OnClickMediaContext);

  if (!media.thumbnail_url) {
    return (
      <Placeholder
        media={media}
        onClick={() => onClickMedia?.(props.media)}
        {...rest}
      />
    );
  }

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
    return <Placeholder media={media} {...rest} />;
  }

  const src = (useThumbnail ? media.thumbnail_url : media.url) ?? "#";

  const fitStyle = {
    cover: "object-cover",
    contain: "object-contain",
  }[image?.fit ?? media.fit ?? "cover"];

  return (
    <img
      src={src}
      alt={media.description ?? ""}
      {...addClass(rest, fitStyle)}
    />
  );
};

const VideoView = (props: MediaViewProps) => {
  const { media, ...rest } = props;
  return <video src={media.url} muted controls {...rest} />;
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
    <a href={media.url} download {...rest}>
      <Placeholder media={media} className="size-full">
        <div className="column items-center">
          {onlyIf(media.name, (name) => (
            <h3>{name}</h3>
          ))}
          <p>Click to download</p>
        </div>
      </Placeholder>
    </a>
  );
};

const Placeholder = (props: { media: MediaFile } & DivProps) => {
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
