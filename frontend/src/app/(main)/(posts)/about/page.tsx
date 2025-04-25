import PostPage from "../_components/post";
import { Metadata } from "next";
import React from "react";
import { getOr404 } from "@/api";

const get = async () => getOr404("/api/about/");

export default async function Page() {
  const about = await get();

  return (
    <PostPage
      post={about}
      options={{
        showPublishedDate: false,
      }}
    />
  );
}

export async function generateMetadata(): Promise<Metadata> {
  const post = await get();

  return {
    title: post.title || "About",
    description: post.subtitle,
  };
}
