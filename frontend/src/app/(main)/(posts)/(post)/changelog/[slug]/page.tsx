import { Metadata } from "next";
import { ChangelogDetail } from "@/api/types";
import { PostPage } from "@/features/posts";
import { AppLink } from "../../_components";
import { SlugParams, generatePostMetadata } from "../../util";
import { getChangelog } from "./get";

export default async function Page(params: SlugParams) {
  const changelog = await getChangelog(params);

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

export async function generateMetadata(params: SlugParams): Promise<Metadata> {
  const changelog = await getChangelog(params);

  return generatePostMetadata(changelog, {
    title: `${changelog.app.title} ${changelog.version}`,
    description: `Changelog for app ${changelog.app.title} version ${changelog.version}`,
  });
}
