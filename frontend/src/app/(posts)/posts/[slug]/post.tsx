import { InlineLink, TintedButton } from "@/components/button";
import { HtmlContent, PublishingStatus } from "@/components/data/post";
import { PostDetail } from "@/components/data/types";
import Webmentions from "@/components/data/webmentions";
import { Date } from "@/components/datetime";
import DangerousHtml from "@/components/html";
import { RemoteIcon } from "@/components/icon";
import MediaCarousel from "@/components/media/media-carousel";
import MediaView from "@/components/media/media-view";
import Optional from "@/components/optional";
import Prose, { ProseClassName } from "@/components/prose";
import itemTheme from "@/components/themed/item-theme";
import { navigationHref } from "@/navigation";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import styles from "./post.module.css";

export default function PostPage({ post }: PostProps) {
  return (
    <main className="h-entry">
      <TintedButton href={post.dev_admin} icon="MB" />
      <PublishingStatus post={post} />
      <InvisiblePostMetadata post={post} />

      <article
        style={itemTheme(post)}
        className={classes(
          styles.postGridAreas,
          "mb-48 px-edge lg:px-0 grid gap-x-8 gap-y-8 justify-center",
          "grid-cols-[min(100%,var(--spacing-readable))]",
          "lg:grid-cols-[1fr_var(--spacing-readable)_240px_1fr]",
        )}
      >
        <DangerousHtml
          html={post.hero_html}
          className="col-start-1 col-span-full row-start-1"
        />
        <Optional
          value={post.hero_image}
          also={!post.hero_html}
          block={(hero) => (
            <MediaView
              media={hero}
              video={{ autoPlay: true, loop: true }}
              className="[grid-area:hero] card max-h-[50vh] readable"
            />
          )}
        />

        <PostTitle post={post} className="[grid-area:title]" />
        <PostInfo post={post} className="[grid-area:info] text-sm" />

        <HtmlContent
          post={post}
          className={
            `[grid-area:content] ${ProseClassName} e-content
          [&_section]:first:*:first:mt-0` /* Remove margin from first item in first section, override for tailwind-prose */
          }
        />

        <MediaCarousel
          media={post.files}
          className="[grid-area:media] h-[50vh] -px-prose"
        />

        <PostWebmentions post={post} className="[grid-area:mentions]" />
      </article>
      <DangerousHtml html={post.content_script} className="hidden" />
    </main>
  );
}

interface PostProps {
  post: PostDetail;
}
const PostTitle = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props, "pretty-prose");
  return (
    <Prose {...rest}>
      <Optional
        value={post.title}
        block={(title) => (
          <h1 className="p-name" style={{ marginBottom: "0" }}>
            {title}
          </h1>
        )}
      />
      <Optional
        value={post.subtitle}
        block={(subtitle) => (
          <div className="p-summary prose-lead">{subtitle}</div>
        )}
      />
    </Prose>
  );
};

const PostInfo = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;
  return (
    <div {...rest}>
      <span className="text-current/80 lg:block lg:mb-2">
        Published <Date date={post.published_at} />
      </span>

      <PostLinks post={post} className="row gap-x-2 flex-wrap" />
      <PostTags post={post} className="row gap-x-2 flex-wrap" />
    </div>
  );
};

const PostLinks = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props, "text-base");

  return (
    <div {...rest}>
      {post.links.map((link) => (
        <InlineLink
          key={link.url}
          href={link.url}
          icon={onlyIf(link.icon, (icon) => (
            <RemoteIcon src={icon} />
          ))}
        />
      ))}
    </div>
  );
};

const PostTags = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props, "text-base");

  return (
    <div {...rest}>
      {post.tags.map((tag) => (
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

const InvisiblePostMetadata = ({ post }: PostProps) => {
  return (
    <div className="hidden">
      <a className="u-url" href={post.url} />
    </div>
  );
};

const PostWebmentions = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;
  return (
    <Optional
      value={post.mentions}
      block={(mentions) => (
        <div {...rest}>
          <h3>Webmentions</h3>
          <Webmentions mentions={mentions} />
        </div>
      )}
    />
  );
};
