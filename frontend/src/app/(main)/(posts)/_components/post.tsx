import parseHtml from "html-react-parser";
import Link from "next/link";
import { AutoHCard } from "@/app/_components/h-card";
import { InlineLink } from "@/components/button";
import { PublishingStatus } from "@/components/data/posts";
import Post from "@/components/data/posts/post";
import {
  AppDetail,
  AppPreview,
  ChangelogDetail,
  PostDetail,
  isApp,
  isChangelog,
} from "@/components/data/types";
import Webmentions from "@/components/data/webmentions";
import { Date } from "@/components/datetime";
import DangerousHtml from "@/components/html";
import { RemoteIcon, RemoteIconProps } from "@/components/icon";
import MediaCarousel from "@/components/media/media-carousel";
import MediaView from "@/components/media/media-view";
import Optional from "@/components/optional";
import { ProseClassName } from "@/components/prose";
import itemTheme from "@/components/themed/item-theme";
import RemoteIFrame from "@/components/third-party/embedded";
import { navigationHref } from "@/navigation";
import { type Optional as MakeOptional } from "@/types";
import { DivPropsNoChildren, PropsExcept } from "@/types/react";
import { addClass, classes } from "@/util/transforms";
import styles from "./post.module.css";

const Insets = "px-edge xl:px-0";
type Post = PostDetail | AppDetail | ChangelogDetail;

interface Options {
  showPublishedDate?: boolean;
}
interface PostProps {
  post: Post;
  options?: Options;
}
interface AppProps {
  app: AppDetail;
}

export default function PostPage(props: PostProps) {
  const { post, options } = props;
  const themeSource = isChangelog(post) && !post.theme ? post.app : post;

  return (
    <div style={itemTheme(themeSource)}>
      <PublishingStatus post={post} />

      <main className={classes("mb-24", "grid", styles.postGridAreas)}>
        <article
          className={classes(
            "h-entry grid subgrid-span-full gap-y-4 w-full",
            styles.postGridAreas,
          )}
        >
          <PostMetadata post={post} />
          <HeroHtml
            post={post}
            className="col-start-1 col-span-full row-start-1 max-h-[50vh]"
          />
          <Hero post={post} className="[grid-area:hero] card max-h-[50vh]" />

          <PostTitle
            post={post}
            className={classes("[grid-area:title]", Insets)}
          />
          <PostInfo
            post={post}
            options={options}
            className={classes(
              "@container [grid-area:info] text-sm xl:text-end xl:*:justify-end xl:*:justify-self-end",
              Insets,
              "xl:pe-edge",
            )}
          />

          <MainContent
            post={post}
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
          post={post}
          className={classes("[grid-area:mentions] mt-8", Insets)}
        />

        {isApp(post) && (
          <Changelogs
            app={post}
            className="[grid-area:changelogs] readable mx-auto"
          />
        )}
      </main>

      <DangerousHtml html={post.content_script} className="hidden" />
    </div>
  );
}

const PostTitle = (props: PostProps & DivPropsNoChildren) => {
  const { post, options, ...rest } = props;

  const _isChangelog = isChangelog(post);
  if (!post.title && !post.subtitle && !_isChangelog) return null;

  return (
    <div {...addClass(rest, "space-y-0.5")}>
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
  const { post, options = {}, ...rest } = props;
  const { showPublishedDate = true } = options;

  return (
    <div {...addClass(rest, "empty:hidden")}>
      {showPublishedDate && (
        <span className="text-current/80 xl:block xl:mb-2">
          Published <Date date={post.published_at} />
        </span>
      )}

      {isApp(post) && post.script && (
        <AppLink app={post} liveInstance={true} className="my-2" />
      )}
      {isChangelog(post) && (
        <AppLink app={post.app} liveInstance={false} className="my-2" />
      )}

      <PostLinks post={post} className="row gap-x-2 flex-wrap" />
      <PostTags post={post} className="row gap-x-2 flex-wrap" />
    </div>
  );
};

const PostMetadata = (props: PostProps) => {
  const { post } = props;

  return (
    <div className="hidden">
      <Link className="u-url" href={post.url} />
    </div>
  );
};

const AppLink = (
  props: {
    app: Pick<AppPreview, "title" | "icon" | "url" | "theme">;
    liveInstance: boolean;
  } & PropsExcept<"a", "children" | "href">,
) => {
  const {
    app,
    liveInstance, // If true, link to the webapp instance page
    style,
    ...rest
  } = addClass(
    props,
    "grid grid-cols-[auto_1fr] hover-extra-background w-fit text-start hover-extra-background before:-inset-2",
  );

  return (
    <Link
      href={liveInstance ? `${app.url}/live` : app.url}
      style={itemTheme(app)}
      target="_blank"
      {...rest}
    >
      <OptionalRemoteIcon
        src={app.icon?.url}
        mask={false}
        className="text-4xl me-2"
      />
      <div>
        <div className="font-bold">{app.title}</div>
        <div className="text-current/80">
          {liveInstance ? "Live instance" : "App"}
        </div>
      </div>
    </Link>
  );
};

const PostLinks = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props, "text-base");
  if (!post.links.length) return null;

  return (
    <div {...rest}>
      {post.links.map((link) => (
        <InlineLink
          key={link.url}
          href={link.url}
          icon={<OptionalRemoteIcon src={link.icon} />}
        />
      ))}
    </div>
  );
};

const OptionalRemoteIcon = (
  props: MakeOptional<RemoteIconProps, "src"> & DivPropsNoChildren,
) => {
  const { src: propsSrc, mask, ...rest } = props;
  return (
    <Optional
      value={propsSrc}
      block={(src) => <RemoteIcon src={src} mask={mask} {...rest} />}
    />
  );
};

const PostTags = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = addClass(props, "text-base");
  if (!post.tags.length) return null;

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

const HeroHtml = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;
  if (isApp(post) && post.is_widget && post.script) {
    const liveUrl = `${post.url}/live`;
    return (
      <iframe
        src={liveUrl}
        title={`Live instance of app '${post.title}'`}
        {...addClass(rest, "w-full")}
      />
    );
  }

  return <DangerousHtml html={post.hero_html} {...rest} />;
};
const Hero = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;

  if (post.hero_embedded_url) {
    return (
      <RemoteIFrame
        src={post.hero_embedded_url}
        {...rest}
        iframeClassName={classes(rest.className, "w-full aspect-video")}
      />
    );
  }

  return (
    <Optional
      value={post.hero_image}
      also={!post.hero_html}
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

const Changelogs = (props: AppProps & DivPropsNoChildren) => {
  const { app, ...rest } = props;
  if (!app.changelog.length) return null;

  return (
    <div {...rest}>
      <h2 className={classes("prose-h2", Insets)}>Changelog</h2>

      <div className="space-y-8">
        {app.changelog.map((entry) => (
          <Post key={entry.url} post={{ ...entry, is_preview: false }} />
        ))}
      </div>
    </div>
  );
};

const MainContent = (props: PostProps & DivPropsNoChildren) => {
  const { post, ...rest } = props;

  if (!post.content_html) return null;

  const content = parseHtml(post.content_html, {
    replace: (domNode) => {
      if (domNode.type === "comment") {
        const value = domNode.nodeValue.trim();
        if (value === "h-card") {
          return <AutoHCard showDetail={true} />;
        }
      }
    },
  });

  return <div {...rest}>{content}</div>;
};
