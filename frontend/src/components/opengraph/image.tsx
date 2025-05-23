import { Property } from "csstype";
import { ImageResponse } from "next/og";
import { CSSProperties } from "react";
import { MediaFile } from "@/api/types";
import { absoluteUrl } from "@/navigation";
import { Nullish } from "@/types";
import { DivProps, Props } from "@/types/react";
import { getPlaintextSummaryFromHtml } from "./text";

type BasicDivProps = Pick<DivProps, "style" | "children">;

const Colors = {
  Background: "#252225",
  Foreground: "#dbdbdf",
  Scrim: "#252225cc",
};

const Size = {
  width: 1200,
  height: 627,
};

const EdgeMargin = "8px";
const FontSize = 64;
const LineHeightEm = 1.3;

interface OpengraphImageProps {
  image?: MediaFile | undefined;
  icon?: MediaFile | undefined;
  text?: string | undefined;
  accentColor?: string | undefined;
}

export const opengraphImage = (props?: OpengraphImageProps) =>
  new ImageResponse(<Content {...props} />, { ...Size });

const Content = (props: OpengraphImageProps) => {
  const { text, image, icon, accentColor = "#55c191" } = props ?? {};

  const textContent = text ? getPlaintextSummaryFromHtml(text) : text;

  if (icon) {
    return (
      <Container>
        <Img
          url={icon.url}
          fit="contain"
          accentColor={accentColor}
          size={192}
        />
        <Text text={textContent} maxLines={2} />
      </Container>
    );
  }

  const isImage = image?.type === "image";
  const isVideo = image?.type === "video";
  const imageUrl = isImage
    ? image.url
    : isVideo
      ? image.thumbnail_url
      : undefined;

  if (!textContent && !imageUrl) {
    return (
      <Container showWatermark={false}>
        <DefaultImage width={Size.height / 2} />
      </Container>
    );
  }

  if (!imageUrl) {
    return (
      <Container>
        <Text text={textContent} maxLines={4} />
      </Container>
    );
  }

  return (
    <Container>
      <Img
        url={imageUrl}
        fit={image?.fit}
        accentColor={accentColor}
        style={{
          borderLeft: `4px solid ${accentColor}`,
          borderRight: `4px solid ${accentColor}`,
        }}
      />

      <div
        style={{
          display: "flex",
          position: "absolute",
          bottom: EdgeMargin,
          backgroundColor: Colors.Scrim,
          borderRadius: FontSize / 4,
        }}
      >
        <Text
          text={textContent}
          maxLines={1}
          style={{ margin: `${FontSize / 6}px ${FontSize / 2}px` }}
        />
      </div>
    </Container>
  );
};

const Container = ({
  style,
  children,
  showWatermark = true,
}: BasicDivProps & { showWatermark?: boolean }) => {
  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: Colors.Background,
        color: Colors.Foreground,
        fontSize: FontSize,
        lineHeight: `${LineHeightEm * FontSize}px`,
        fontWeight: 600,
        ...style,
      }}
    >
      {children}
      {showWatermark && <Watermark />}
    </div>
  );
};

const Img = ({
  url,
  fit,
  accentColor,
  size = Size.height,
  style = {},
}: {
  url: string | Nullish;
  fit: Property.ObjectFit | Nullish;
  accentColor: string;
  size?: number;
  style?: CSSProperties;
}) => {
  if (!url) return null;

  return (
    <img
      src={absoluteUrl(url)}
      height={size}
      alt=""
      style={{
        objectFit: fit ?? "cover",
        ...style,
      }}
    />
  );
};

const DefaultImage = (
  props: Pick<Props<"svg">, "width" | "fill" | "style">,
) => {
  const { width, fill = Colors.Foreground, style } = props;
  return (
    <svg viewBox="0 0 16 11.28" width={width} style={style}>
      <path
        style={{ fill }}
        d="m2.64 3.75.05.59q.55-.71 1.47-.71.95 0 1.34.86.54-.86 1.55-.86 1.67 0 1.71 2.31v4.15h-1.66v-4.05q0-.55-.15-.78-.16-.24-.52-.24-.46 0-.69.57l.01.2v4.3h-1.66v-4.04q0-.54-.14-.78-.15-.25-.52-.25-.43 0-.68.46v4.61h-1.66v-6.34z"
      />
      <path
        style={{ fill }}
        d="m14.91 7.13q0 1.56-.5 2.26-.5.8-1.5.8-.8 0-1.3-.7l-.1.6h-1.52v-9h1.62v3.18q.5-.64 1.3-.64 1 0 1.5.77.5.76.5 2.24zm-1.6-.42q0-1-.2-1.34-.2-.35-.7-.35t-.8.48v2.89q.3.4.8.4t.7-.3.2-1.18z"
      />
    </svg>
  );
};

const Watermark = () => {
  return (
    <DefaultImage
      width={96}
      style={{ position: "absolute", bottom: EdgeMargin, right: EdgeMargin }}
    />
  );
};

const Text = (
  props: BasicDivProps & { text: string | undefined; maxLines: number },
) => {
  const { text, maxLines, style } = props;

  if (!text) return null;

  return (
    <div
      style={
        {
          textAlign: "center",
          overflow: "hidden",
          textOverflow: "ellipsis",
          display: "-webkit-box",
          "-webkit-box-orient": "vertical",
          "-webkit-line-clamp": maxLines,
          maxWidth: Size.height,
          maxHeight: `${FontSize * LineHeightEm * maxLines}px`,
          ...style,
        } as CSSProperties
      }
    >
      {getPlaintextSummaryFromHtml(text)}
    </div>
  );
};
