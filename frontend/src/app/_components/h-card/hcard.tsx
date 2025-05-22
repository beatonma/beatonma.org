import React from "react";
import { GlobalState } from "@/api/types";
import { Date } from "@/components/datetime";
import { Row } from "@/components/layout";
import MediaView from "@/components/media/media-view";
import ExternalLink from "@/components/third-party/link";
import * as microformats from "@/microformats";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";
import styles from "./hcard.module.css";

type GlobalHCard = NonNullable<GlobalState["hcard"]>;

export default function HCard(
  props: DivPropsNoChildren<{
    hcard: GlobalHCard | Nullish;
    showDetail: boolean;
  }>,
) {
  const { hcard, showDetail = false, ...rest } = props;

  if (!hcard) return null;

  return (
    <div
      {...addClass(
        rest,
        microformats.H["h-card"],
        "card card-content surface",
        styles.hcardGrid,
        "grid-cols-[auto_1fr]",
      )}
    >
      <HCardImages hcard={hcard} className="[grid-area:image] me-4" />

      <div className="[grid-area:info]">
        <div className={classes("text-xl", microformats.HCard["p-name"])}>
          {hcard.name}
        </div>
        <div className="text-sm">
          <HAdr hadr={hcard.location} />
        </div>
      </div>

      <div className="[grid-area:relme] divider-['_-_'] text-sm">
        <span>
          <ExternalLink
            href={hcard.url}
            className={microformats.HCard["u-url"]}
          />
        </span>
        {onlyIf(
          showDetail,
          hcard.relme.map((it) => (
            <span key={it.url} className="[--link-color:var(--fg)]">
              <ExternalLink rel="me" href={it.url} formatStyle="brand" />
            </span>
          )),
        )}
      </div>

      <div className="hidden">
        {/* Values available for parsers but not displayed directly */}
        <Date className={microformats.HCard["dt-bday"]} date={hcard.birthday} />
      </div>
    </div>
  );
}

const HCardImages = (props: DivPropsNoChildren<{ hcard: GlobalHCard }>) => {
  const { hcard, ...rest } = props;

  if (!hcard.photo && !hcard.logo) return null;
  const mainImageClass =
    "absolute w-(--image-size) rounded-md border-2 border-vibrant/50";

  return (
    <div
      {...addClass(rest, "max-w-(--image-size) max-h-(--image-size) relative")}
    >
      {onlyIf(hcard.photo, (photo) => (
        <MediaView media={photo} className={mainImageClass} />
      ))}
      {onlyIf(hcard.logo, (logo) => (
        <div
          className={
            hcard.photo
              ? "absolute size-[calc(var(--image-size)/5)] m-2 bottom-0 right-0 "
              : mainImageClass
          }
        >
          <MediaView media={logo} className="rounded-md" />
        </div>
      ))}
    </div>
  );
};

const HAdr = (props: DivPropsNoChildren<{ hadr: GlobalHCard["location"] }>) => {
  const { hadr, ...rest } = props;

  if (!hadr) return null;

  return (
    <Row {...addClass(rest, "divider-[','] gap-x-ch flex-wrap *:shrink-0")}>
      {onlyIf(hadr.locality, (locality) => (
        <span className={microformats.HCard["p-locality"]}>{locality}</span>
      ))}
      {onlyIf(hadr.region, (region) => (
        <span className={microformats.HCard["p-region"]}>{region}</span>
      ))}
      {onlyIf(hadr.country, (country) => (
        <span className={microformats.HCard["p-country-name"]}>{country}</span>
      ))}
    </Row>
  );
};
