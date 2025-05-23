import { Metadata } from "next";
import PostPage from "@/app/(main)/(posts)/(post)/_components/post";
import {
  type SlugParams,
  generatePostMetadata,
} from "@/app/(main)/(posts)/(post)/util";
import { getPost } from "./get";

export default async function Page(params: SlugParams) {
  const app = await getPost(params);

  return <PostPage post={app} />;
}

export async function generateMetadata(params: SlugParams): Promise<Metadata> {
  const post = await getPost(params);

  return generatePostMetadata(post);
}
