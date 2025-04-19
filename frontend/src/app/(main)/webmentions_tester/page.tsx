import { Metadata } from "next";
import { getOrThrow } from "@/api";
import WebmentionsTesterPage from "@/app/(main)/webmentions_tester/webmentions-tester";
import { navigationHref } from "@/navigation";

export const metadata: Metadata = {
  title: "Webmentions Tester",
  description: "Test your webmentions setup",
};

export default async function Page() {
  const { mentions, temporary_outgoing_mentions: tempMentions } =
    await getOrThrow("/api/webmentions_tester/", {
      query: { url_path: navigationHref("webmentionsTest") },
    });

  return (
    <WebmentionsTesterPage mentions={mentions} tempMentions={tempMentions} />
  );
}
