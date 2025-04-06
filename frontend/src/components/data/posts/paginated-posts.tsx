import { Query, client } from "@/api";
import Optional from "@/components/optional";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import InfinitePosts from "./infinite-posts";

export interface PaginatedPostsProps {
  query?: Query<"/api/posts/">;
}
export default async function PaginatedPosts(
  props: PaginatedPostsProps & DivPropsNoChildren,
) {
  const { query, ...rest } = props;

  // Load first page on server side
  const initial = await client.GET("/api/posts/", {
    params: {
      query: query,
    },
  });
  const data = initial.data;
  if (!data) throw initial.error;

  const title =
    onlyIf(query?.query, (q) => `'${q}'`) ??
    onlyIf(query?.tag, (tag) => `#${tag}`);

  // Hand off to InfinitePosts to handle pagination.
  return (
    <div {...rest}>
      <Optional value={title} block={(_title) => <h2>{_title}</h2>} />
      <InfinitePosts init={data} query={query} />
    </div>
  );
}
