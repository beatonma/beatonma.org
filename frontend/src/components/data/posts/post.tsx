import { InlineButton, InlineLink } from "@/components/button";
import { PostPreview } from "@/components/data/types";
import { Date } from "@/components/datetime";
import { Row } from "@/components/layout";
import MediaPreview from "@/components/media/media-preview";
import Optional from "@/components/optional";
import { ProseClassName } from "@/components/prose";
import itemTheme from "@/components/themed/item-theme";
import RemoteIFrame from "@/components/third-party/embedded";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import { HtmlContent, PostType, PublishingStatus } from "./components";

export default function Post(
  props: { post: PostPreview } & DivPropsNoChildren,
) {
  const { post, style, ...rest } = addClass(props, "h-entry");
  const themedStyle = { ...style, ...itemTheme(post) };

  return (
    <article style={themedStyle} {...rest}>
      <div className="card-hover surface">
        <PublishingStatus post={post} />
        <PostMediaPreview post={post} className="max-h-[60vh]" />

        <div className="card-content column gap-1">
          <Optional
            value={post.title}
            block={(title) => (
              <Row className="gap-x-4 items-center">
                <h2 className="p-name">
                  <InlineLink href={post.url} icon={null}>
                    {title}
                  </InlineLink>
                </h2>
                <PostType post={post} className="text-current/60" />
              </Row>
            )}
          />

          <HtmlContent
            post={post}
            className={
              post.is_preview
                ? `text-lg! p-summary ${ProseClassName} compact`
                : `text-xl! e-content ${ProseClassName} compact`
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
    </article>
  );
}

const PostMediaPreview = (
  props: { post: PostPreview } & DivPropsNoChildren,
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
      <MediaPreview
        media={[post.hero_image]}
        {...addClass(rest, "surface-muted")}
      />
    );
  }
  return (
    <MediaPreview media={post.files} {...addClass(rest, "surface-muted")} />
  );
};
