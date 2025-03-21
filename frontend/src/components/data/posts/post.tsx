import { ComponentPropsWithRef, useId } from "react";
import { HtmlContent, PublishingStatus } from "@/components/data/post";
import { PostPreview } from "@/components/data/types";
import { Date } from "@/components/datetime";
import MediaPreview from "@/components/media/media-preview";
import Optional from "@/components/optional";
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
      <a
        href={post.url}
        aria-labelledby={labelId}
        className="card-hover surface block"
      >
        <PublishingStatus post={post} />
        <PostMediaPreview post={post} />

        <div className="card-content column gap-1">
          <Optional
            value={post.title}
            block={(title) => (
              <h2 className="p-name" id={labelId}>
                {title}
              </h2>
            )}
          />

          <HtmlContent
            post={post}
            id={onlyIf(!post.title, labelId)}
            className={post.is_preview ? "p-summary" : "text-lg e-content"}
          />

          <Date
            date={post.published_at}
            className="text-sm text-current/60 self-end"
          />
        </div>
      </a>
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
