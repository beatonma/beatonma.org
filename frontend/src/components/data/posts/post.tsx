import { ComponentPropsWithRef, useId } from "react";
import { InlineButton, InlineLink } from "@/components/button";
import { HtmlContent, PublishingStatus } from "@/components/data/post";
import { PostPreview } from "@/components/data/types";
import { Date } from "@/components/datetime";
import { AppIcon } from "@/components/icon";
import { Row } from "@/components/layout";
import MediaPreview from "@/components/media/media-preview";
import Optional from "@/components/optional";
import { ProseClassName } from "@/components/prose";
import itemTheme from "@/components/themed/item-theme";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

export default function Post(
  props: { post: PostPreview } & ComponentPropsWithRef<"div">,
) {
  const { post, style, ...rest } = addClass(props, "h-entry");
  const themedStyle = { ...style, ...itemTheme(post) };
  const labelId = useId();

  return (
    <article style={themedStyle} {...rest}>
      <div className="card-hover surface">
        <PublishingStatus post={post} />
        <PostMediaPreview post={post} className="max-h-[60vh]" />

        <div className="card-content column gap-1">
          <Optional
            value={post.title}
            block={(title) => (
              <h2 className="p-name" id={labelId}>
                <InlineLink href={post.url} icon={postIcon(post)}>
                  {title}
                </InlineLink>
              </h2>
            )}
          />

          <HtmlContent
            post={post}
            id={onlyIf(!post.title, labelId)}
            className={
              post.is_preview
                ? "text-lg! p-summary"
                : `text-xl! e-content ${ProseClassName}`
            }
          />

          <Row className="justify-between mt-4">
            {post.is_preview ? (
              <InlineButton href={post.url}>Read more</InlineButton>
            ) : (
              <InlineButton
                href={post.url}
                icon="Link"
                title="Link to this post"
              />
            )}

            <Date
              date={post.published_at}
              className="text-sm text-current/60 self-end"
            />
          </Row>
        </div>
      </div>

      <h4>{post.post_type}</h4>
    </article>
  );
}

const postIcon = (post: PostPreview) => {
  const icons: Record<PostPreview["post_type"], AppIcon | undefined> = {
    app: "Code",
    changelog: "Code",
    post: undefined,
  };
  return icons[post.post_type];
};

const PostMediaPreview = (
  props: { post: PostPreview } & ComponentPropsWithRef<"div">,
) => {
  const { post, ...rest } = addClass(props, "bg-muted");
  if (!post.hero_image && !post.files.length) return null;

  if (post.hero_image) {
    return <MediaPreview media={[post.hero_image]} {...rest} />;
  }
  return <MediaPreview media={post.files} {...rest} />;
};
