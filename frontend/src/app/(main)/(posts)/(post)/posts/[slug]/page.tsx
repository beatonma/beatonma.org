import { Metadata } from "next";
import { getSlug } from "@/api";
import PostPage from "@/app/(main)/(posts)/(post)/_components/post";

interface Params {
  slug: string;
}

const get = async (params: Promise<Params>) =>
  getSlug("/api/posts/{slug}/", params);

export default async function Page({ params }: { params: Promise<Params> }) {
  const app = await get(params);

  return <PostPage post={app} />;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const post = await get(params);

  return {
    title: post.title || "Post",
    description: post.subtitle,
  };
}
