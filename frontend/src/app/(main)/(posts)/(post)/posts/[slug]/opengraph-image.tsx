import { type SlugParams } from "@/app/(main)/(posts)/(post)/util";
import { opengraphImage } from "@/features/nextjs";
import { getPost } from "./get";

export default async function Image(params: SlugParams) {
  const post = await getPost(params);

  return opengraphImage({
    image: post.hero_image ?? post.files?.[0],
    text: post.title ?? post.content_html ?? undefined,
    accentColor: post.theme?.vibrant ?? undefined,
  });
}
