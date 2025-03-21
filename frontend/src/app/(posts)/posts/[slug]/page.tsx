import { client } from "@/api";
import PostPage from "./post";

interface Params {
  slug: string;
}

export default async function Page({ params }: { params: Promise<Params> }) {
  const { slug } = await params;

  const response = await client.GET("/api/posts/{slug}/", {
    params: {
      path: { slug },
    },
  });
  const post = response.data;

  if (!post) throw response.error;

  return <PostPage post={post} />;
}
