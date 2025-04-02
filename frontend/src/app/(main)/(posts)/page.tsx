import { Metadata } from "next";
import { Query } from "@/api";
import PaginatedPosts from "@/components/data/posts";

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

  return (
    <main className="grid grid-cols-[1fr_min(100%,60ch)_1fr] [grid-template-areas:'._posts_.']">
      <PaginatedPosts
        query={params}
        className="grid grid-cols-1 gap-8 [grid-area:posts] h-feed"
      />
    </main>
  );
}
