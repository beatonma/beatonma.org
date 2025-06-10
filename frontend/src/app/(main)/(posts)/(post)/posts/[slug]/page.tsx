import { Metadata } from "next";
import { PostPage } from "@/features/posts";
import { type SlugParams, generatePostMetadata } from "../../util";
import { getPost } from "./get";

export default async function Page(params: SlugParams) {
  const app = await getPost(params);

  return <PostPage post={app} />;
}

export async function generateMetadata(params: SlugParams): Promise<Metadata> {
  const post = await getPost(params);

  return generatePostMetadata(post);
}
