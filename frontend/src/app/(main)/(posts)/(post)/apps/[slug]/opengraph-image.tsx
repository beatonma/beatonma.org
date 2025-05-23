import { SlugParams } from "@/app/(main)/(posts)/(post)/util";
import { opengraphImage } from "@/components/opengraph/image";
import { getApp } from "./get";

export default async function Image(params: SlugParams) {
  const post = await getApp(params);

  return opengraphImage({
    icon: post.icon ?? undefined,
    image: post.hero_image ?? post.files?.[0],
    text: post.title ?? post.content_html ?? undefined,
    accentColor: post.theme?.vibrant ?? undefined,
  });
}
