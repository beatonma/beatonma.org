import { Metadata, ResolvingMetadata } from "next";
import React from "react";
import { getOr404 } from "@/api";
import { resolveSlug } from "@/api/client";
import { AboutDetail } from "@/api/types";
import { InlineLink } from "@/components/button";
import Optional from "@/components/optional";
import Prose from "@/components/prose";
import { PostPage } from "@/features/posts";
import { DivPropsNoChildren } from "@/types/react";
import { classes } from "@/util/transforms";
import { generatePostMetadata } from "../../util";

type Params = { params: Promise<{ slug: string[] | undefined }> };

export default async function Page(params: Params) {
  const about = await get(params);

  return <AboutPage about={about} />;
}

export const generateMetadata = async (
  params: Params,
  parent: ResolvingMetadata,
): Promise<Metadata> => {
  const post = await get(params);
  const parentMeta = await parent;

  const meta = await generatePostMetadata(post, {
    title: post.title || "About",
    description: post.subtitle || undefined,
  });

  return {
    ...meta,
    openGraph: {
      ...meta.openGraph,
      images: parentMeta.openGraph?.images,
    },
    robots: !!post.parent ? { index: false } : undefined,
  };
};

const AboutPage = ({ about }: { about: AboutDetail }) => (
  <PostPage
    post={about}
    customContent={{
      extraContent: (context) => (
        <AboutNavigation
          className={classes("card card-content surface-alt mt-16")}
          about={about}
        />
      ),
    }}
    options={{
      showPublishedDate: false,
    }}
  />
);

const AboutNavigation = (props: DivPropsNoChildren<{ about: AboutDetail }>) => {
  const { about, ...rest } = props;

  if (!about.parent && !about.children.length) return null;

  return (
    <div {...rest}>
      <Prose className="[--link-color:var(--fg)] text-sm">
        <h2>Explore</h2>

        <Optional
          value={about.parent}
          block={(parent) => (
            <div>
              <InlineLink href={parent.url} icon={null}>
                {parent.title || "/about/"}
              </InlineLink>
            </div>
          )}
        />

        <ul>
          <li className="">
            {"> "}
            {about.title || "/about/"}
          </li>
          <ul>
            {about.children.map((child) => (
              <li key={child.path}>
                <InlineLink href={child.url} icon={null}>
                  {child.title}
                </InlineLink>
              </li>
            ))}
          </ul>

          {about.siblings.map((sibling) => (
            <li key={sibling.path}>
              <InlineLink href={sibling.url} icon={null}>
                {sibling.title}
              </InlineLink>
            </li>
          ))}
        </ul>
      </Prose>
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
