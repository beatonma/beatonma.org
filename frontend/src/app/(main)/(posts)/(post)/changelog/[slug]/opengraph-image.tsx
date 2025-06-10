import { SlugParams } from "@/app/(main)/(posts)/(post)/util";
import { opengraphImage } from "@/features/nextjs";
import { getChangelog } from "./get";

export default async function Image(params: SlugParams) {
  const post = await getChangelog(params);

  return opengraphImage({
    icon: post.app?.icon ?? undefined,
    text: post.title ?? post.content_html ?? undefined,
    accentColor: post.theme?.vibrant ?? post.app.theme?.vibrant ?? undefined,
  });
}
