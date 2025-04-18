import PostPage from "../_components/post";
import { Metadata } from "next";
import { getOr404 } from "@/api";

const get = async () => getOr404("/api/about/");

export default async function Page() {
  const app = await get();

  return <PostPage post={app} />;
}

export async function generateMetadata(): Promise<Metadata> {
  const post = await get();

  return {
    title: post.title || "Post",
    description: post.subtitle,
  };
}
