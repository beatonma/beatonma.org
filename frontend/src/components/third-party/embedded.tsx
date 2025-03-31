"use client";

import {
  ComponentPropsWithoutRef,
  ReactNode,
  useEffect,
  useState,
} from "react";
import ExternalLink from "@/components/third-party/link";
import RemoteContent, {
  RemoteContentProvider,
} from "@/components/third-party/remote-content";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

type IFrameProps = ComponentPropsWithoutRef<"iframe">;
interface EmbeddedProps {
  src: string;
  iframeClassName?: string;
}
interface EmbeddedRemoteContentProvider {
  provider: (src: string, contentId: string) => RemoteContentProvider;
}

type EmbeddedProviderProps = { contentId: string } & IFrameProps;

export default function RemoteIFrame(
  props: EmbeddedProps & Omit<DivPropsNoChildren, "content">,
) {
  const { src, iframeClassName, ...rest } = props;
  const [provider, setProvider] = useState<
    RemoteContentProvider | null | undefined
  >(undefined);
  const [content, setContent] = useState<() => ReactNode>();

  useEffect(() => {
    for (const host of RecognisedHosts) {
      const [regex, _provider, _content] = host;
      const match = regex.exec(src);
      const contentId = match?.groups?.["content_id"];

      if (contentId) {
        setProvider(_provider.provider(src, contentId));
        setContent(
          () => () => _content({ contentId, className: iframeClassName }),
        );
        break;
      }
    }
  }, [src, iframeClassName]);

  if (!provider) return null;
  if (!content) return null;

  return (
    <RemoteContent
      provider={provider}
      content={content}
      {...addClass(rest, "border-dashed border-2 border-current/10")}
    />
  );
}

const YoutubeContentProvider: EmbeddedRemoteContentProvider = {
  provider: (src, contentId) => ({
    domain: "youtube-nocookie.com",
    description: (
      <>
        A YouTube{" "}
        <ExternalLink referrer href={src}>
          video
        </ExternalLink>{" "}
        is embedded here.
      </>
    ),
  }),
};

const EmbeddedYoutubeVideo = (props: EmbeddedProviderProps) => {
  const { contentId, ...rest } = props;
  return (
    <iframe
      src={`https://www.youtube-nocookie.com/embed/${contentId}`}
      title="YouTube video player"
      allow="clipboard-write; encrypted-media; picture-in-picture; web-share"
      referrerPolicy="strict-origin-when-cross-origin"
      allowFullScreen
      {...rest}
    />
  );
};

const RecognisedHosts: [
  RegExp,
  EmbeddedRemoteContentProvider,
  (props: EmbeddedProviderProps) => ReactNode,
][] = [
  [
    /^(https:\/\/)?(www\.)?youtube.com\/watch\?v=(?<content_id>[^&]+)/,
    YoutubeContentProvider,
    EmbeddedYoutubeVideo,
  ],
  [
    /^(https:\/\/)?(www\.)?youtu.be\/(?<content_id>[^?&]+)/,
    YoutubeContentProvider,
    EmbeddedYoutubeVideo,
  ],
  [
    /^(https:\/\/)?(www\.)?youtube-nocookie.com\/embed\/(?<content_id>[^/?&])/,
    YoutubeContentProvider,
    EmbeddedYoutubeVideo,
  ],
];
