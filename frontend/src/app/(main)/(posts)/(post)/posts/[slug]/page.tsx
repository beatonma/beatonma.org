import { Metadata } from "next";
import { PostPage } from "@/features/posts";
import Repository, { SlugParams } from "@/repository";
import { generatePostMetadata } from "../../util";

export default async function Page(params: SlugParams) {
  const app = await Repository.posts.getPost(params);

  return <PostPage post={app} />;
}

export async function generateMetadata(params: SlugParams): Promise<Metadata> {
  const post = await Repository.posts.getPost(params);

  return generatePostMetadata(post);
}
