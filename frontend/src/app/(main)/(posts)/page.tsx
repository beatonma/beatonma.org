import { Metadata } from "next";
import { Query } from "@/api/types";
import { Optional } from "@/components/optional";
import { PaginatedPosts } from "@/features/posts";
import { navigationHref } from "@/navigation";
import { onlyIf } from "@/util/optional";
import { classes } from "@/util/transforms";
import { Github, PointsOfInterest } from "./_components";
import styles from "./page.module.css";

type SearchParams = Promise<Query<"/api/posts/">>;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: SearchParams;
}): Promise<Metadata> {
  const search = (await searchParams)!;
  const { query, tag, feed } = search;

  const alternates: Metadata["alternates"] = {
    canonical: navigationHref("posts"),
    types: {
      "application/rss+xml": [
        {
          url: navigationHref("feed", { query, tag, feed }), // Link to feed with same filters applied, no pagination
          title: "RSS feed",
        },
      ],
    },
  };

  const description = ["Posts by Michael Beaton"];
  if (feed) {
    description.push(`categorised as '${feed}'`);
  }
  if (tag) {
    description.push(`tagged with #${tag}`);
  }
  if (query) {
    description.push(`containing '${query}'`);
  }
  const hasMultipleFilters =
    [!!feed, !!tag, !!query].filter(Boolean).length > 1;

  return {
    title: hasMultipleFilters
      ? "Posts"
      : feed ||
        onlyIf(query, `'${query}'`) ||
        onlyIf(tag, `#${tag}`) ||
        "Posts",
    description: description.join(", "),
    alternates,
  };
}

export default async function Page({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;

  const showExtras = !params?.offset && !params?.tag && !params?.query;

  return (
    <main className={styles.mainFeedGrid}>
      <PaginatedPosts
        query={params}
        className="[grid-area:posts] grid grid-cols-1 space-y-8 gap-x-8 h-feed"
      />
      <Optional
        value={showExtras}
        block={() => (
          <>
            <PointsOfInterest
              className={classes(
                "[grid-area:poi] [--poi-gap:calc(var(--spacing)*4)] gap-x-(--poi-gap)",
                "row gap-x-4 *:shrink-0 overflow-x-auto overflow-y-hidden max-xl:px-edge",
                "xl:flex-wrap",
              )}
            />
            <Github className="[grid-area:github] max-xl:card max-xl:card-content max-xl:surface-alt" />
          </>
        )}
      />
    </main>
  );
}
