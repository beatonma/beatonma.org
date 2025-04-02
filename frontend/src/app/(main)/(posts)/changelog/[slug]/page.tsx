import PostPage from "../../_components/post";
import { Metadata } from "next";
import { getSlug } from "@/api";

interface Params {
  slug: string;
}

const get = async (params: Promise<Params>) =>
  getSlug("/api/changelog/{slug}/", params);

export default async function Page({ params }: { params: Promise<Params> }) {
  const changelog = await get(params);

  return <PostPage post={changelog} />;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const changelog = await get(params);

  return {
    title: `${changelog.app.title} ${changelog.version}`,
    description: `Changelog for app ${changelog.app.title} version ${changelog.version}`,
  };
}
