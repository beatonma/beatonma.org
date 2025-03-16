import { Query, client } from "@/api";
import InfinitePosts from "@/components/data/infinite-posts";
import { DivPropsNoChildren } from "@/types/react";

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

  // Hand off to InfinitePosts to handle pagination.
  return (
    <div {...rest}>
      <InfinitePosts init={data} query={query} />
    </div>
  );
}
