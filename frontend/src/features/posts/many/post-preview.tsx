import Link from "next/link";
import { type PostPreview as PostPreviewType } from "@/api/types";
import { ButtonProps, InlineButton } from "@/components/button";
import { Date, formatDate } from "@/components/datetime";
import { Row } from "@/components/layout";
import { Optional } from "@/components/optional";
import { ProseClassName } from "@/components/prose";
import { RemoteIFrame } from "@/components/third-party";
import { MediaGroupPreview } from "@/features/media";
import { itemTheme } from "@/features/themed";
import { DivPropsNoChildren } from "@/types/react";
import { addClass, classes } from "@/util/transforms";
import { HtmlContent, PostType, PublishingStatus } from "../components";

export const PostPreview = (
  props: DivPropsNoChildren<{ post: PostPreviewType }>,
) => {
  const { post, style, ...rest } = props;
  const themedStyle = { ...style, ...itemTheme(post) };

  return (
    <article style={themedStyle} {...addClass(rest, "h-entry")}>
      <div className="card-hover surface relative isolate">
        <Link
          href={post.url}
          className="absolute inset-0 z-0"
          aria-label={getLabelForPost(post)}
        />

        <PublishingStatus post={post} />
        <PostMediaPreview post={post} className="max-h-[60vh] z-1 relative" />

        <div className="card-content column gap-1 z-1 relative">
          <Optional
            value={post.title}
            block={(title) => (
              <Row className="gap-x-4 items-center">
                <h2 className="p-name">
                  <Link href={post.url} aria-hidden tabIndex={-1}>
                    {title}
                  </Link>
                </h2>
                <PostType post={post} className="text-current/60" />
              </Row>
            )}
          />

          <HtmlContent
            post={post}
            className={classes(
              "compact z-1",
              ProseClassName,
              post.is_preview ? "text-lg! p-summary" : "text-xl! e-content",
            )}
          />

          <Row className="justify-between mt-4">
            <LinkToPost post={post} aria-hidden tabIndex={-1} />

            <Date
              date={post.published_at}
              className="text-sm text-current/60 self-end"
            />
          </Row>
        </div>
      </div>
    </article>
  );
};

const LinkToPost = (props: { post: PostPreviewType } & ButtonProps) => {
  const { post, ...rest } = props;
  const common: ButtonProps = {
    href: post.url,
    "aria-label": getLabelForPost(post),
    title: "Link to this post",
    ...rest,
  };

  if (post.is_preview) {
    return <InlineButton {...common}>Read more</InlineButton>;
  }
  return <InlineButton {...common} icon="Link" />;
};

const PostMediaPreview = (
  props: DivPropsNoChildren<{ post: PostPreviewType }>,
) => {
  const { post, ...rest } = props;
  if (!post.hero_embedded_url && !post.hero_image && !post.files.length)
    return null;

  if (post.hero_embedded_url) {
    return (
      <RemoteIFrame
        src={post.hero_embedded_url}
        iframeClassName="w-[calc(100%+1px)] aspect-video" /* w-full can show a line of background at edge of frame, add a pixel to prevent that */
        {...addClass(rest, "card-content surface-alt")}
      />
    );
  }
  if (post.hero_image) {
    return (
      <MediaGroupPreview
        media={[post.hero_image]}
        {...addClass(rest, "surface-muted")}
      />
    );
  }
  return (
    <MediaGroupPreview
      media={post.files}
      {...addClass(rest, "surface-muted")}
    />
  );
};

/** If a post does not have a title, try to build something descriptive. */
const getLabelForPost = (post: PostPreviewType): string => {
  const postType = post.post_type === "post" ? null : `(${post.post_type})`;
  if (post.title) return [post.title, postType].filter(Boolean).join(" ");

  const labelParts = ["Untitled post"];
  if (post.hero_embedded_url) {
    labelParts.push("with embedded URL");
  } else if (post.files.length) {
    labelParts.push("with media");
  }

  return labelParts.join(" ") + `, dated ${formatDate(post.published_at)}`;
};
