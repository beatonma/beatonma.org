import PostPage from "../../_components/post";
import { Metadata } from "next";
import { getSlug } from "@/api";

interface Params {
  slug: string;
}

export default async function Page({ params }: { params: Promise<Params> }) {
  const app = await get(params);

  return <PostPage post={app} />;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const app = await get(params);

  return {
    title: app.title,
    description: app.subtitle,
  };
}

const get = async (params: Promise<Params>) =>
  getSlug("/api/apps/{slug}/", params);
