import { Metadata } from "next";
import { Query } from "@/api";
import Github from "@/app/(main)/(posts)/_components/github";
import PointsOfInterest from "@/app/(main)/(posts)/_components/poi";
import PaginatedPosts from "@/components/data/posts";
import Optional from "@/components/optional";
import { classes } from "@/util/transforms";
import styles from "./page.module.css";

type SearchParams = Promise<Query<"/api/posts/">>;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: SearchParams;
}): Promise<Metadata> {
  const { query, tag } = (await searchParams)!;

  if (tag) {
    return {
      title: `#${tag}`,
      description: `Posts tagged with #${tag}`,
    };
  }
  if (query) {
    return {
      title: `${query}`,
      description: `Results for search query '${query}'`,
    };
  }

  return {
    title: "Home",
    description: "Posts by Michael Beaton",
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
