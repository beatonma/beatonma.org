import { Metadata } from "next";
import { getSlug } from "@/api";
import { ChangelogDetail } from "@/api/types";
import PostPage, { AppLink } from "@/app/(main)/(posts)/(post)/_components";

interface Params {
  slug: string;
}

const get = async (params: Promise<Params>) =>
  getSlug("/api/changelog/{slug}/", params);

export default async function Page({ params }: { params: Promise<Params> }) {
  const changelog = await get(params);

  const post: ChangelogDetail = {
    ...changelog,
    theme: changelog.theme ? changelog.theme : changelog.app.theme,
  };

  return (
    <PostPage
      post={post}
      customContent={{
        extraInfo: (
          <AppLink app={post.app} liveInstance={false} className="my-2" />
        ),
      }}
    />
  );
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
