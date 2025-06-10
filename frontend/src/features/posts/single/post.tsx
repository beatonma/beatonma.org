import parseHtml from "html-react-parser";
import Link from "next/link";
import { ReactNode } from "react";
import type { DetailedPost, PostDetail } from "@/api/types";
import { AutoHCard } from "@/app/_components/h-card";
import { InlineLink } from "@/components/button";
import { Date } from "@/components/datetime";
import DangerousHtml from "@/components/html";
import { RemoteIcon } from "@/components/icon";
import Optional from "@/components/optional";
import { ProseClassName } from "@/components/prose";
import { RemoteIFrame } from "@/components/third-party";
import { MediaCarousel, MediaView } from "@/features/media";
import { itemTheme } from "@/features/themed";
import { Webmentions } from "@/features/webmentions";
import { navigationHref } from "@/navigation";
import { Nullish } from "@/types";
import { ClassNameProps, DivPropsNoChildren } from "@/types/react";
import { addClass, classes } from "@/util/transforms";
import { PublishingStatus } from "../components";
import styles from "./post.module.css";

const Insets = "px-edge xl:px-0";

interface Options {
  showPublishedDate?: boolean;
}

type Post = Pick<
  DetailedPost,
  | "post_type"
  | "title"
  | "subtitle"
  | "url"
  | "is_published"
  | "published_at"
  | "theme"
  | "hero_embedded_url"
  | "hero_image"
  | "hero_html"
  | "content_html"
  | "content_script"
  | "files"
  | "links"
  | "tags"
  | "mentions"
>;
type PostTitle = Pick<Post, "title" | "subtitle">;
type PostHeroHtml = Pick<Post, "hero_html">;
type PostMetadata = Pick<Post, "url">;
type PostMainContent = Pick<Post, "content_html">;
type PostLinks = Pick<Post, "links">;
type PostTags = Pick<Post, "tags">;
type PostInfo = Pick<Post, "published_at"> &
  PostLinks &
  PostTags & {
    options: Options | Nullish;
    extraInfo: ReactNode;
  };
type PostMentions = Pick<Post, "mentions">;
type PostHero = Pick<Post, "hero_embedded_url" | "hero_image"> & {
  customHero: ((className: string | undefined) => ReactNode) | Nullish;
};

type CustomContent = Partial<Pick<PostInfo, "extraInfo">> &
  Partial<Pick<PostHero, "customHero">> & {
    extraContent?: (context: { insetsClass: string }) => ReactNode;
  };

export const PostPage = (props: {
  post: Post;
  customContent?: CustomContent;
  options?: Options;
}) => {
  const { post, customContent, options } = props;
  return (
    <div style={itemTheme(post.theme)}>
      <PublishingStatus post={post} />

      <main className={classes("mb-24 grid", styles.postGridAreas)}>
        <article
          className={classes(
            "h-entry grid subgrid-span-full gap-y-4 w-full",
            styles.postGridAreas,
          )}
        >
          <PostMetadata url={post.url} />
          <HeroHtml
            hero_html={post.hero_html}
            className="col-start-1 col-span-full row-start-1 row-end-1 max-h-[50vh]"
          />
          <Optional
            value={!post.hero_html}
            block={() => (
              <Hero
                hero_image={post.hero_image}
                hero_embedded_url={post.hero_embedded_url}
                customHero={customContent?.customHero}
                className="[grid-area:hero] max-h-[50vh] card surface"
              />
            )}
          />

          <PostTitle
            title={post.title}
            subtitle={post.subtitle}
            className={classes("[grid-area:title]", Insets)}
          />
          <PostInfo
            published_at={post.published_at}
            links={post.links}
            tags={post.tags}
            options={options}
            extraInfo={customContent?.extraInfo}
            className={classes(
              "@container [grid-area:info] text-sm xl:text-end xl:*:justify-end xl:*:justify-self-end",
              Insets,
              "xl:pe-edge",
            )}
          />

          <PostMainContent
            content_html={post.content_html}
            className={classes(
              "@container",
              "[grid-area:content]",
              "e-content",
              ProseClassName,
              Insets,
            )}
          />

          <MediaCarousel
            media={post.files}
            className="[grid-area:media] max-h-[80vh]"
          />
        </article>

        <PostWebmentions
          mentions={post.mentions}
          className={classes("[grid-area:mentions] mt-8", Insets)}
        />

        <Optional
          value={customContent?.extraContent}
          block={(extraContent) => (
            <div className="[grid-area:contentextra] readable mx-auto">
              {extraContent({ insetsClass: Insets })}
            </div>
          )}
        />
      </main>

      <DangerousHtml html={post.content_script} className="hidden" />
    </div>
  );
};

const PostTitle = (props: DivPropsNoChildren<PostTitle>) => {
  const { title, subtitle, ...rest } = props;

  return (
    <div {...addClass(rest, "space-y-0.5")}>
      <Optional
        value={title}
        block={(title) => <h1 className="p-name">{title}</h1>}
      />
      <Optional
        value={subtitle}
        block={(subtitle) => <p className="p-summary prose-lead">{subtitle}</p>}
      />
    </div>
  );
};

const PostInfo = (props: DivPropsNoChildren<PostInfo>) => {
  const { published_at, links, tags, options, extraInfo, ...rest } = props;
  const { showPublishedDate = true } = options ?? {};

  return (
    <div {...addClass(rest, "empty:hidden")}>
      {showPublishedDate && (
        <span className="text-current/80 xl:block xl:mb-2">
          Published <Date date={published_at} />
        </span>
      )}

      {extraInfo}

      <PostLinks links={links} className="row gap-x-2 flex-wrap" />
      <PostTags tags={tags} className="row gap-x-2 flex-wrap" />
    </div>
  );
};

const PostMetadata = (props: PostMetadata) => {
  const { url } = props;

  return (
    <div className="hidden">
      <Link className="u-url" href={url} />
    </div>
  );
};

const PostLinks = (props: DivPropsNoChildren<PostLinks>) => {
  const { links, ...rest } = addClass(props, "text-base");
  if (!links.length) return null;

  return (
    <div {...rest}>
      {links.map((link) => (
        <InlineLink
          key={link.url}
          href={link.url}
          icon={
            <Optional
              value={link.icon}
              block={(src) => <RemoteIcon src={src} />}
            />
          }
        />
      ))}
    </div>
  );
};

const PostTags = (props: DivPropsNoChildren<PostTags>) => {
  const { tags, ...rest } = addClass(props, "text-base");
  if (!tags.length) return null;

  return (
    <div {...rest}>
      {tags.map((tag) => (
        <Tag key={tag.name} tag={tag} />
      ))}
    </div>
  );
};

const Tag = ({ tag }: { tag: PostDetail["tags"][number] }) => (
  <InlineLink key={tag.name} icon="Tag" href={navigationHref("tag", tag.name)}>
    {tag.name}
  </InlineLink>
);

const PostWebmentions = (props: DivPropsNoChildren<PostMentions>) => {
  const { mentions, ...rest } = addClass(props);
  return (
    <Optional
      value={mentions}
      block={(mentions) => (
        <aside {...rest}>
          <h3>Webmentions</h3>

          <Webmentions mentions={mentions} />
        </aside>
      )}
    />
  );
};

const HeroHtml = (props: DivPropsNoChildren<PostHeroHtml>) => {
  const { hero_html, ...rest } = props;

  return <DangerousHtml html={hero_html} {...rest} />;
};

const Hero = (props: ClassNameProps & PostHero) => {
  const { hero_embedded_url, hero_image, customHero, ...rest } = props;

  if (hero_embedded_url) {
    return (
      <RemoteIFrame
        src={hero_embedded_url}
        {...rest}
        iframeClassName={classes(rest.className, "w-full aspect-video")}
      />
    );
  }

  if (customHero) {
    return customHero(rest?.className);
  }

  return (
    <Optional
      value={hero_image}
      block={(hero) => (
        <MediaView
          media={hero}
          video={{ autoPlay: true, loop: true }}
          {...rest}
        />
      )}
    />
  );
};

const PostMainContent = (props: DivPropsNoChildren<PostMainContent>) => {
  const { content_html, ...rest } = props;

  if (!content_html) return null;

  return (
    <div {...rest}>
      {parseHtml(content_html, {
        replace: (domNode) => {
          if (domNode.type !== "comment") return;

          const value = domNode.nodeValue.trim();
          if (value === "h-card") {
            return <AutoHCard showDetail={true} />;
          }

          const remote = (
            <RemoteIFrame
              src={value}
              className="card card-content surface-alt"
              iframeClassName="w-full aspect-video"
            />
          );
          if (remote) return remote;
        },
      })}
    </div>
  );
};
