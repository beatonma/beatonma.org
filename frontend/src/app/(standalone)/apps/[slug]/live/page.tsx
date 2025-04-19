import { Metadata } from "next";
import { notFound } from "next/navigation";
import Script from "next/script";
import { getSlug } from "@/api";
import DangerousHtml from "@/components/html";

interface Params {
  slug: string;
}

const get = async (params: Promise<Params>) => {
  return getSlug("/api/apps/{slug}/", params);
};

export default async function Page({ params }: { params: Promise<Params> }) {
  const app = await get(params);

  if (!app.script) return notFound();

  return (
    <>
      <noscript>
        This page is supposed to show a webapp but you do not have javascript
        enabled.
      </noscript>
      <DangerousHtml html={app.script_html} />
      <Script src={app.script} defer async />
    </>
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const app = await get(params);

  return {
    title: app.title,
    description: app.subtitle,
  };
}
