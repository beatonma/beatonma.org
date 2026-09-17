import { Metadata, ResolvingMetadata } from "next";
import { InlineLink } from "@/components/button";
import { Optional } from "@/components/optional";
import { Prose } from "@/components/prose";
import { PostPage } from "@/features/posts";
import Repository, { SlugParams } from "@/repository";
import { AboutDetail } from "@/repository/types";
import { DivPropsNoChildren } from "@/types/react";
import { generatePostMetadata } from "../../util";

type Params = SlugParams;

export default async function Page(params: Params) {
  const about = await getPage(params);

  return <AboutPage about={about} />;
}

export const generateMetadata = async (
  params: Params,
  parent: ResolvingMetadata,
): Promise<Metadata> => {
  const post = await getPage(params);
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
          className="card card-content surface-alt mt-16"
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

const getPage = async ({ params }: Params) => {
  return Repository.posts.getAboutPage(params);
};
