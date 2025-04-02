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
      <DangerousHtml html={app.script_html} />
      <Script src={app.script} />
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
