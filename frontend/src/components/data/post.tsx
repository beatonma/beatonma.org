import { ComponentPropsWithRef } from "react";
import { InlineButton } from "@/components/button";
import { PostPreview } from "@/components/data/types";
import { Date } from "@/components/datetime";
import { Row } from "@/components/layout";
import MediaPreview from "@/components/media/media-preview";
import itemTheme from "@/components/themed/item-theme";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

export default function Posts(
  props: { posts: PostPreview[] } & DivPropsNoChildren,
) {
  const { posts, ...rest } = props;
  return (
    <div {...rest}>
      {posts.map((post) => (
        <Post key={post.url} post={post} />
      ))}
    </div>
  );
}

export function Post(
  props: { post: PostPreview } & ComponentPropsWithRef<"div">,
) {
  const { post, style, ...rest } = addClass(
    props,
    "card surface h-entry e-content",
  );

  const themedStyle = { ...style, ...itemTheme(post) };

  return (
    <article style={themedStyle} {...rest}>
      {onlyIf(
        !post.is_published,
        <div className="p-4 bg-red-600 text-white">
          This post has not been published
        </div>,
      )}

      <PostMediaPreview post={post} />

      <div className="card-content column gap-1">
        {onlyIf(post.title, (title) => (
          <h2>{title}</h2>
        ))}
        {onlyIf(post.content_html, (__html) => (
          <div dangerouslySetInnerHTML={{ __html }} />
        ))}

        <Row className="justify-between gap-4 mt-2">
          <Row className="gap-4">
            {onlyIf(
              post.is_preview,
              <InlineButton href={post.url}>Read more</InlineButton>,
            )}
            <InlineButton href={post.dev_admin} icon="MB" />
          </Row>

          <Date date={post.published_at} className="text-sm text-current/60" />
        </Row>
      </div>
    </article>
  );
}

const PostMediaPreview = (
  props: { post: PostPreview } & ComponentPropsWithRef<"div">,
) => {
  const { post, ...rest } = addClass(
    props,
    "overflow-hidden rounded-md bg-muted",
  );
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
