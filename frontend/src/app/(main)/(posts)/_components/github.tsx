import { GithubActivity } from "@/features/github";
import Repository from "@/repository";
import { DivPropsNoChildren } from "@/types/react";

export const Github = async (props: DivPropsNoChildren) => {
  const data = await Repository.getGithubRecent();
  if (!data) return null;

  return <GithubActivity activity={data} {...props} />;
};
