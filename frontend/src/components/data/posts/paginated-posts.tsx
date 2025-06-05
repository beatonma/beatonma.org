import { getOrNull, getOrThrow } from "@/api";
import { Query } from "@/api/types";
import Optional from "@/components/optional";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import InfinitePosts from "./infinite-posts";

export interface PaginatedPostsProps {
  query?: Query<"/api/posts/">;
}
export default async function PaginatedPosts(
  props: DivPropsNoChildren<PaginatedPostsProps>,
) {
  const { query, ...rest } = props;

  const data = await getOrThrow("/api/posts/", {
    query,
  });
  const state = await getOrNull("/api/state/");

  const title = [
    onlyIf(query?.tag, (tag) => `#${tag}`),
    onlyIf(query?.query, (q) => `'${q}'`),
  ]
    .filter(Boolean)
    .join(", ");

  // Hand off to InfinitePosts to handle pagination.
  return (
    <div {...rest}>
      <Optional value={title} block={(_title) => <h2>{_title}</h2>} />
      <InfinitePosts init={data} query={query} feeds={state?.feeds} />
    </div>
  );
}
