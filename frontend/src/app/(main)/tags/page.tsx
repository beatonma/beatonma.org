import { Metadata } from "next";
import { getOrNull } from "@/api";
import { InlineLink } from "@/components/button";
import { Prose } from "@/components/prose";
import { navigationHref } from "@/navigation";

export const metadata: Metadata = {
  title: "Tags",
  description: "Explore posts by tag",
};

export default async function Page() {
  const tags = await getOrNull("/api/tags/");
  return (
    <main className="mb-24">
      <Prose className="mx-auto">
        <h2>Tags</h2>
        {tags
          ?.sort((a, b) => b.count - a.count)
          ?.map((tag) => (
            <div key={tag.name}>
              <InlineLink
                icon={tag.count}
                href={navigationHref("tag", tag.name)}
              >
                {tag.name}
              </InlineLink>
            </div>
          )) || <div>Nothing here</div>}
      </Prose>
    </main>
  );
}
