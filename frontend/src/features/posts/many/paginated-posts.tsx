import { Optional } from "@/components/optional";
import Repository from "@/repository";
import { getDataOrNull } from "@/repository/result";
import { FeedQuery } from "@/repository/types";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { InfinitePosts } from "./infinite-posts";

export interface PaginatedPostsProps {
  query?: FeedQuery;
}

export const PaginatedPosts = async (
  props: DivPropsNoChildren<PaginatedPostsProps>,
) => {
  const { query, ...rest } = props;

  const data = await getDataOrNull(
    await Repository.posts.getPaginatedPosts(query),
  );
  const state = await Repository.getGlobalState();

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
      <InfinitePosts
        init={data ?? undefined}
        query={query}
        feeds={state?.feeds}
      />
    </div>
  );
};
