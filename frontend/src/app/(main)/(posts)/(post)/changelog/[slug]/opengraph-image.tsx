import { opengraphImage } from "@/features/nextjs";
import Repository, { SlugParams } from "@/repository";

export default async function Image(params: SlugParams) {
  const post = await Repository.posts.getChangelog(params);

  return opengraphImage({
    icon: post.app?.icon ?? undefined,
    text: post.title ?? post.content_html ?? undefined,
    accentColor: post.theme?.vibrant ?? post.app.theme?.vibrant ?? undefined,
  });
}
