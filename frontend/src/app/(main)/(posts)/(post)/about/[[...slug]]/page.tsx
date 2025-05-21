import { Metadata } from "next";
import React from "react";
import { getOr404 } from "@/api";
import { resolveSlug } from "@/api/client";
import { AboutDetail } from "@/api/types";
import PostPage from "@/app/(main)/(posts)/(post)/_components/post";
import { InlineLink } from "@/components/button";
import { DivPropsNoChildren } from "@/types/react";

type Params = { params: Promise<{ slug: string[] | undefined }> };

export default async function Page(params: Params) {
  const about = await get(params);

  return <AboutPage about={about} />;
}

export async function generateMetadata(params: Params): Promise<Metadata> {
  const post = await get(params);

  return {
    title: post.title || "About",
    description: post.subtitle,
  };
}

const AboutPage = ({ about }: { about: AboutDetail }) => (
  <PostPage
    post={about}
    customContent={{
      extraContent: (context) => (
        <AboutNavigation className={context.insetsClass} about={about} />
      ),
    }}
    options={{
      showPublishedDate: false,
    }}
  />
);

const AboutNavigation = (props: DivPropsNoChildren<{ about: AboutDetail }>) => {
  const { about, ...rest } = props;
  return (
    <div {...rest}>
      {about.children.map((child) => (
        <InlineLink key={child.title} href={child.url} icon={null}>
          {child.title}
        </InlineLink>
      ))}
    </div>
  );
};

const get = async ({ params }: Params) => {
  const slug = await resolveSlug(params);

  if (slug) {
    return getOr404("/api/about/{path}", { path: { path: slug } });
  }
  return getOr404("/api/about/");
};
