import { Metadata } from "next";
import { notFound } from "next/navigation";
import Script from "next/script";
import { DangerousHtml } from "@/components/html";
import Repository from "@/repository";

interface Params {
  slug: string;
}

export default async function Page({ params }: { params: Promise<Params> }) {
  const app = await Repository.posts.getApp(params);

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
  const app = await Repository.posts.getApp(params);

  return {
    title: app.title,
    description: app.subtitle,
  };
}
