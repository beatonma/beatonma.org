import Link from "next/link";
import { AppPreview } from "@/api/types";
import { RemoteIcon } from "@/components/icon";
import Optional from "@/components/optional";
import itemTheme from "@/components/themed/item-theme";
import { Props } from "@/types/react";
import { addClass } from "@/util/transforms";

export const AppLink = (
  props: Props<
    "a",
    {
      app: Pick<AppPreview, "title" | "icon" | "url" | "theme">;
      liveInstance: boolean;
    },
    "children" | "href"
  >,
) => {
  const {
    app,
    liveInstance, // If true, link to the webapp instance page
    style,
    ...rest
  } = addClass(
    props,
    "grid grid-cols-[auto_1fr] hover-extra-background w-fit text-start before:-inset-2",
  );

  return (
    <Link
      href={liveInstance ? `${app.url}/live` : app.url}
      style={itemTheme(app)}
      target="_blank"
      {...rest}
    >
      <Optional
        value={app.icon?.url}
        block={(src) => (
          <RemoteIcon src={src} mask={false} className="text-4xl me-2" />
        )}
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
