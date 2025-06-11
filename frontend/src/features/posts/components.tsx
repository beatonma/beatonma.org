import { DetailedPost, PreviewPost } from "@/api/types";
import { DangerousHtml } from "@/components/html";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

type Post = PreviewPost | DetailedPost;

export const HtmlContent = (
  props: Omit<
    DivPropsNoChildren<{ post: Pick<Post, "content_html"> }>,
    "dangerouslySetInnerHTML"
  >,
) => {
  const { post, ...rest } = props;
  return <DangerousHtml html={post.content_html} {...rest} />;
};

export const PublishingStatus = (
  props: DivPropsNoChildren<{ post: Pick<Post, "is_published"> }>,
) => {
  const { post, ...rest } = addClass(props, "p-4 bg-red-600 text-white");
  return onlyIf(
    !post.is_published,
    <div {...rest}>This post has not been published</div>,
  );
};

export const PostType = (
  props: DivPropsNoChildren<{ post: Pick<Post, "post_type"> }>,
) => {
  const { post, ...rest } = addClass(
    props,
    "text-xs badge badge-content border-1",
  );

  if (post.post_type === "post") return null;
  if (post.post_type === "changelog")
    return <span {...rest}>{post.post_type}</span>;

  return <span {...rest}>{post.post_type}</span>;
};
