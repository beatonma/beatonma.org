import { Metadata } from "next";
import { navigationHref } from "@/navigation";
import Repository from "@/repository";
import { WebmentionsTesterPage } from "./webmentions-tester";

export const metadata: Metadata = {
  title: "Webmentions Tester",
  description: "Test your webmentions setup",
};

export default async function Page() {
  const { mentions, temporary_outgoing_mentions: tempMentions } =
    await Repository.getWebmentionsTester(navigationHref("webmentionsTest"));

  return (
    <WebmentionsTesterPage mentions={mentions} tempMentions={tempMentions} />
  );
}
