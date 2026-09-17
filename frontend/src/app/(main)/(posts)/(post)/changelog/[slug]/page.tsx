import { Metadata } from "next";
import { PostPage } from "@/features/posts";
import Repository, { SlugParams } from "@/repository";
import { ChangelogDetail } from "@/repository/types";
import { AppLink } from "../../_components";
import { generatePostMetadata } from "../../util";

export default async function Page(params: SlugParams) {
  const changelog = await Repository.posts.getChangelog(params);

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
  const changelog = await Repository.posts.getChangelog(params);

  return generatePostMetadata(changelog, {
    title: `${changelog.app.title} ${changelog.version}`,
    description: `Changelog for app ${changelog.app.title} version ${changelog.version}`,
  });
}
