import PostPage from "../_components/post";
import { Metadata } from "next";
import { notFound } from "next/navigation";
import { client } from "@/api";

const get = async () => {
  const response = await client.GET("/api/about/");
  const data = response.data;

  if (!data) return notFound();
  return data;
};

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
