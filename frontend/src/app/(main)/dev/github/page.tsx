import { Metadata } from "next";
import { SampleGithub } from "@/app/(main)/dev/_sample";
import { GithubActivity } from "@/features/github";

export const metadata: Metadata = {
  title: "Github activity",
  description: "",
};

export default async function Page() {
  return <GithubActivity activity={SampleGithub} />;
}
