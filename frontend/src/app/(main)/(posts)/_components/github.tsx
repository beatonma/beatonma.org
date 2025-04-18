import { getOrNull } from "@/api";
import GithubActivity from "@/components/data/github/github";
import { DivPropsNoChildren } from "@/types/react";

export default async function Github(props: DivPropsNoChildren) {
  const data = await getOrNull("/api/github/recent/");
  if (!data) return null;

  return <GithubActivity activity={data} {...props} />;
}
