import Link from "next/link";
import { ComponentPropsWithoutRef } from "react";
import { InlineButton, InlineLink } from "@/components/button";
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
      <PublishingStatus post={post} />
      <PostMetadata post={post} />

      <article style={itemTheme(post)} className="mb-48">
        <Hero post={post} className="w-full h-auto mb-8" />

        <Post post={post} />
      </article>
    </main>
  );
}

interface PostProps {
  post: PostDetail;
}
const Post = (props: PostProps & ComponentPropsWithoutRef<"article">) => {
  const { post, style, ...rest } = addClass(props, "");

  return (
    <div {...rest}>
      <Prose elementName="article">
        <div className="space-y-1">
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

          <div className="text-sm">
            <span className="text-current/80">
              Published <Date date={post.published_at} />
            </span>

            <PostTags post={post} className="row gap-2" />
            <PostLinks post={post} className="row gap-2" />
          </div>
        </div>

        <HtmlContent post={post} className="e-content" />
      </Prose>

      <MediaCarousel media={post.files} className="h-[50vh]" />
      <Webmentions mentions={post.mentions} className="px-edge" />

      <DangerousHtml html={post.content_script} className="hidden" />
    </div>
  );
};

const Hero = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;

  if (post.hero_image) {
    return (
      <MediaView
        media={post.hero_image}
        video={{ autoPlay: true, loop: true }}
        {...addClass(rest, "card readable")}
      />
    );
  }

  if (post.hero_html) {
    return <DangerousHtml html={post.hero_html} {...rest} />;
  }
};

const PostLinks = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props, "text-base");

  return (
    <div {...rest}>
      {onlyIf(post.app, (app) => (
        <InlineButton href={app.url}>{app.title}</InlineButton>
      ))}

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
  <Link key={tag.name} href={navigationHref("tag", tag.name)} className="">
    <span className="before:content-['#'] before:text-current/40 p-category">
      {tag.name}
    </span>
  </Link>
);

const PostMetadata = ({ post }: PostProps) => {
  return (
    <div className="hidden">
      <a className="u-url" href={post.url} />
    </div>
  );
};
