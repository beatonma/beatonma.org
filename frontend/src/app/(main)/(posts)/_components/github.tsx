import { client } from "@/api";
import GithubActivity from "@/components/data/github/github";
import { DivPropsNoChildren } from "@/types/react";

export default async function Github(props: DivPropsNoChildren) {
  const response = await client.GET("/api/github/recent/");

  const data = response.data;
  if (!data) return null;

  return <GithubActivity activity={data} {...props} />;
}
