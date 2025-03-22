import Link from "next/link";
import { ComponentPropsWithoutRef } from "react";
import { InlineButton, InlineLink, TintedButton } from "@/components/button";
import { HtmlContent, PublishingStatus } from "@/components/data/post";
import { PostDetail } from "@/components/data/types";
import Webmentions from "@/components/data/webmentions";
import { Date } from "@/components/datetime";
import DangerousHtml from "@/components/html";
import { RemoteIcon } from "@/components/icon";
import MediaCarousel from "@/components/media/media-carousel";
import MediaView from "@/components/media/media-view";
import Optional from "@/components/optional";
import Prose from "@/components/prose";
import itemTheme from "@/components/themed/item-theme";
import { navigationHref } from "@/navigation";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

export default function PostPage({ post }: PostProps) {
  return (
    <main className="h-entry">
      <TintedButton href={post.dev_admin} icon="MB" />
      <PublishingStatus post={post} />
      <InvisiblePostMetadata post={post} />

      <article
        style={itemTheme(post)}
        className='mb-48 grid gap-x-8
        [grid-template-areas:"hero"_"title"_"info"_"content"]
        lg:[grid-template-areas:"._hero_hero_."_"._title_._."_"._content_info_."]
        lg:grid-cols-[1fr_auto_300px_1fr]
        '
      >
        <Hero post={post} className="mb-8 [grid-area:hero]" />

        <PostTitle post={post} className="[grid-area:title]" />
        <PostInfo post={post} className="text-sm [grid-area:info] px-edge" />

        <div className="readable [grid-area:content] space-y-16">
          <Prose elementName="div">
            <HtmlContent post={post} className="e-content" />
          </Prose>

          <MediaCarousel media={post.files} className="h-[50vh]" />

          <PostWebmentions post={post} className="px-edge" />
        </div>

        <DangerousHtml html={post.content_script} className="hidden" />
      </article>
    </main>
  );
}

interface PostProps {
  post: PostDetail;
}
// const Post = (props: PostProps & ComponentPropsWithoutRef<"article">) => {
//   const { post, style, ...rest } = props;
//
//   return (
//     <div {...rest}>
//       <PostTitle post={post} />
//       <PostInfo post={post} className="text-sm" />
//
//       <Prose elementName="div">
//         <HtmlContent post={post} className="e-content" />
//       </Prose>
//
//       <MediaCarousel media={post.files} className="h-[50vh]" />
//
//       <PostWebmentions post={post} className="px-edge" />
//
//       <DangerousHtml html={post.content_script} className="hidden" />
//     </div>
//   );
// };

const Hero = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;

  if (post.hero_image) {
    return (
      <MediaView
        media={post.hero_image}
        video={{ autoPlay: true, loop: true }}
        {...addClass(rest, "card max-h-[50vh] readable")}
      />
    );
  }

  if (post.hero_html) {
    return <DangerousHtml html={post.hero_html} {...rest} />;
  }
};

const PostTitle = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;
  return (
    <Prose elementName="div" {...rest}>
      <Optional
        value={post.title}
        block={(title) => <h1 className="p-name">{title}</h1>}
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
      <span className="text-current/80">
        Published <Date date={post.published_at} />
      </span>

      <PostLinks post={post} className="row gap-2 flex-wrap" />
      <PostTags post={post} className="row gap-2 flex-wrap" />
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
