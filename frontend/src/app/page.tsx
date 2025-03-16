import { Query } from "@/api";
import PaginatedPosts from "@/components/data/paginated-posts";

type SearchParams = Promise<Query<"/api/posts/">>;
export default async function Page({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;

  return (
    <div className="grid grid-cols-[1fr_min(100%,60ch)_1fr] [grid-template-areas:'._posts_.']">
      <PaginatedPosts
        query={params}
        className="grid grid-cols-1 gap-8 [grid-area:posts]"
      />
    </div>
  );
}
