import DangerousHtml from "@/components/html";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";
import { Post } from "./types";

export const HtmlContent = (
  props: { post: Post } & Omit<DivPropsNoChildren, "dangerouslySetInnerHTML">,
) => {
  const { post, ...rest } = props;
  return <DangerousHtml html={post.content_html} {...rest} />;
};

export const PublishingStatus = (
  props: { post: Post } & DivPropsNoChildren,
) => {
  const { post, ...rest } = addClass(props, "p-4 bg-red-600 text-white");
  return onlyIf(
    !post.is_published,
    <div {...rest}>This post has not been published</div>,
  );
};
