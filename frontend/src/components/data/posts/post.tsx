import { ComponentPropsWithRef, useId } from "react";
import { InlineButton } from "@/components/button";
import { HtmlContent, PublishingStatus } from "@/components/data/post";
import { PostPreview } from "@/components/data/types";
import { Date } from "@/components/datetime";
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
        <PostMediaPreview post={post} />

        <div className="card-content column gap-1">
          <Optional
            value={post.title}
            block={(title) => (
              <h2 className="p-name" id={labelId}>
                <a href={post.url}>{title}</a>
              </h2>
            )}
          />

          <HtmlContent
            post={post}
            id={onlyIf(!post.title, labelId)}
            className={
              post.is_preview
                ? "p-summary"
                : `text-lg e-content ${ProseClassName}`
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

      <a href={post.dev_admin}>admin</a>
    </article>
  );
}

const PostMediaPreview = (
  props: { post: PostPreview } & ComponentPropsWithRef<"div">,
) => {
  const { post, ...rest } = addClass(props, "bg-muted");
  if (!post.hero_image && !post.files.length) return null;

  return (
    <div {...rest}>
      {onlyIf(post.hero_image, (hero) => (
        <MediaPreview media={[hero]} />
      ))}

      {onlyIf(
        !post.hero_image && !post.is_preview,
        <MediaPreview media={post.files} />,
      )}
    </div>
  );
};
