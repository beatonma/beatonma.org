import { InlineLink } from "@/components/button";
import { HtmlContent, PublishingStatus } from "@/components/data/post";
import { PostDetail } from "@/components/data/types";
import Webmentions from "@/components/data/webmentions";
import { Date } from "@/components/datetime";
import DangerousHtml from "@/components/html";
import { RemoteIcon } from "@/components/icon";
import MediaCarousel from "@/components/media/media-carousel";
import MediaView from "@/components/media/media-view";
import Optional from "@/components/optional";
import { ProseClassName } from "@/components/prose";
import itemTheme from "@/components/themed/item-theme";
import { navigationHref } from "@/navigation";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import styles from "./post.module.css";

const Insets = "px-edge lg:px-0";

export default function PostPage({ post }: PostProps) {
  return (
    <div>
      <PublishingStatus post={post} />

      <main
        className={classes(
          "h-entry mb-48",
          styles.postGridAreas,
          "grid gap-x-8 gap-y-8 justify-center",
          "grid-cols-[min(100%,var(--spacing-readable))]",
          "lg:grid-cols-[1fr_var(--spacing-readable)_240px_1fr]",
        )}
      >
        <article
          style={itemTheme(post)}
          className={classes(
            "grid subgrid-span-full",
            styles.postGridAreas,
            Insets,
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
          <PostInfo
            post={post}
            className="[grid-area:info] text-sm lg:text-end lg:*:justify-end"
          />

          <HtmlContent
            post={post}
            className={classes(
              "[grid-area:content]",
              ProseClassName,
              "e-content",
            )}
          />

          <MediaCarousel
            media={post.files}
            className="[grid-area:media] max-h-[80vh]"
          />
        </article>

        <PostWebmentions
          post={post}
          className={classes("[grid-area:mentions]", Insets)}
        />
      </main>

      <DangerousHtml html={post.content_script} className="hidden" />
    </div>
  );
}

interface PostProps {
  post: PostDetail;
}
const PostTitle = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;
  return (
    <div {...rest}>
      <Optional
        value={post.title}
        block={(title) => <h1 className="p-name">{title}</h1>}
      />
      <Optional
        value={post.subtitle}
        block={(subtitle) => <p className="p-summary prose-lead">{subtitle}</p>}
      />
    </div>
  );
};

const PostInfo = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;
  return (
    <div {...rest}>
      <span className="text-current/80 lg:block lg:mb-2">
        Published <Date date={post.published_at} />
      </span>

      <PostLinks post={post} className="row gap-x-2 flex-wrap empty:hidden" />
      <PostTags post={post} className="row gap-x-2 flex-wrap empty:hidden" />

      <div className="hidden">
        <a className="u-url" href={post.url} />
      </div>
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

const PostWebmentions = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props);
  return (
    <Optional
      value={post.mentions}
      block={(mentions) => (
        <aside {...rest}>
          <h3>Webmentions</h3>

          <Webmentions mentions={mentions} />
        </aside>
      )}
    />
  );
};
