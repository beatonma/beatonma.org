import { getOrNull } from "@/api";
import { InlineButton } from "@/components/button";
import hoverUnderlineStyles from "@/components/css/hover-underline.module.css";
import { DivPropsNoChildren } from "@/types/react";
import { formatUrl } from "@/util/format/url";
import { addClass } from "@/util/transforms";
import styles from "./points-of-interest.module.css";

export const PointsOfInterest = async (props: DivPropsNoChildren) => {
  const state = await getOrNull("/api/state/");
  const poi = state?.poi;

  if (!poi?.length) return null;

  return (
    <div
      {...addClass(
        props,
        styles.poi,
        "[--hover:var(--vibrant)] [--underline-thickness:2px]",
        "font-normal [font-variant:all-small-caps]",
      )}
    >
      <span className={styles.poiTitle}>POI:</span>

      {poi.map((it) => (
        <InlineButton
          className={hoverUnderlineStyles.hoverUnderline}
          key={it.url}
          href={it.url}
          icon={it.icon}
        >
          {it.label ?? formatUrl(it.url)}
        </InlineButton>
      ))}
    </div>
  );
};
