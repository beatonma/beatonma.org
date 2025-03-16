import Image from "next/image";
import { ComponentPropsWithRef } from "react";
import { PostPreview } from "@/components/data/types";
import MediaPreview from "@/components/media/media-preview";
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
  const { post, ...rest } = addClass(props, "card surface card-content");

  return (
    <div {...rest}>
      <PostThumbnail image={post.image} />

      <MediaPreview media={post.files} />

      {onlyIf(post.title, (title) => (
        <h2>{title}</h2>
      ))}
      {onlyIf(post.content_html, (__html) => (
        <div dangerouslySetInnerHTML={{ __html }} />
      ))}
    </div>
  );
}

const PostThumbnail = (props: { image: PostPreview["image"] }) => {
  const { image } = props;
  if (!image?.url || image.type !== "image") return null;
  return (
    <img
      src={image.url.replace("https", "http")}
      alt={image.description ?? ""}
    />
  );
};
