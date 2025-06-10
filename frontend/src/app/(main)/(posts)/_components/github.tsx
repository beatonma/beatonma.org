import { getOrNull } from "@/api";
import { GithubActivity } from "@/features/github";
import { DivPropsNoChildren } from "@/types/react";

export const Github = async (props: DivPropsNoChildren) => {
  const data = await getOrNull("/api/github/recent/");
  if (!data) return null;

  return <GithubActivity activity={data} {...props} />;
};
