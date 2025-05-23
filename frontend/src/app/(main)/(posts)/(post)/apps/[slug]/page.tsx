import { Metadata } from "next";
import { CSSProperties } from "react";
import { AppDetail } from "@/api/types";
import PostPage, { AppLink } from "@/app/(main)/(posts)/(post)/_components";
import { SlugParams } from "@/app/(main)/(posts)/(post)/util";
import LocalIFrame from "@/app/(main)/(posts)/_components/LocalIFrame";
import Post from "@/components/data/posts/post";
import Optional from "@/components/optional";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";
import { classes } from "@/util/transforms";
import { getApp } from "./get";

export default async function Page(params: SlugParams) {
  const app = await getApp(params);

  return (
    <PostPage
      post={app}
      customContent={{
        extraInfo: (
          <Optional
            value={app.script}
            block={() => (
              <AppLink app={app} liveInstance={true} className="my-2" />
            )}
          />
        ),
        extraContent: (context) => (
          <Changelogs
            app={app}
            className="readable mx-auto"
            insetsClass={context.insetsClass}
          />
        ),
        customHero: (className) => {
          if (app.is_widget && app.script) {
            const style = parseStyle(app.widget_style);
            return (
              <div style={style} className={classes(className, "w-full")}>
                <LocalIFrame
                  style={iframeStyle(style)}
                  src={`${app.url}/live`}
                  title={`Live instance of app '${app.title}'`}
                  className="w-full"
                />
              </div>
            );
          }
        },
      }}
    />
  );
}

export async function generateMetadata(params: SlugParams): Promise<Metadata> {
  const app = await getApp(params);

  return {
    title: app.title,
    description: app.subtitle,
  };
}

const Changelogs = (
  props: DivPropsNoChildren<{ app: AppDetail; insetsClass: string }>,
) => {
  const { app, insetsClass, ...rest } = props;
  if (!app.changelog.length) return null;

  return (
    <div {...rest}>
      <h2 className={classes("prose-h2", insetsClass)}>Changelog</h2>

      <div className="space-y-8">
        {app.changelog.map((entry) => (
          <Post key={entry.url} post={{ ...entry, is_preview: false }} />
        ))}
      </div>
    </div>
  );
};

const parseStyle = (
  styleString: string | Nullish,
): CSSProperties | undefined => {
  if (!styleString) return undefined;

  const parts = styleString.split(";").filter((it) => it.includes(":"));
  return Object.fromEntries(parts.map((part) => part.split(":")));
};
const iframeStyle = (
  containerStyle: CSSProperties | undefined,
): CSSProperties => ({
  ...containerStyle,
  margin: 0,
  padding: 0,
});
