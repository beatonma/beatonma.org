import { Metadata } from "next";
import { Query } from "@/api";
import Github from "@/app/(main)/(posts)/_components/github";
import PaginatedPosts from "@/components/data/posts";
import Optional from "@/components/optional";
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

  const showGithub = !params?.offset && !params?.tag && !params?.query;

  return (
    <main className={styles.mainFeedGrid}>
      <PaginatedPosts
        query={params}
        className="[grid-area:posts] grid grid-cols-1 gap-8 h-feed"
      />
      <Optional
        value={showGithub}
        block={() => (
          <Github className="[grid-area:github] max-xl:card max-xl:card-content max-xl:surface-alt" />
        )}
      />
    </main>
  );
}
