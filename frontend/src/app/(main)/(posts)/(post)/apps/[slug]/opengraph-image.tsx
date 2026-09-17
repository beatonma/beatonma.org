import { opengraphImage } from "@/features/nextjs";
import Repository, { SlugParams } from "@/repository";

export default async function Image(params: SlugParams) {
  const post = await Repository.posts.getApp(params);

  return opengraphImage({
    icon: post.icon ?? undefined,
    image: post.hero_image ?? post.files?.[0],
    text: post.title ?? post.content_html ?? undefined,
    accentColor: post.theme?.vibrant ?? undefined,
  });
}
