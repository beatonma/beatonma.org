import Link from "next/link";
import React from "react";
import { ResponseOf } from "@/api";
import GlobalMotd from "@/app/(main)/_components/motd";
import ReturnToTopButton from "@/app/(main)/_components/return-to-top";
import GlobalSearch from "@/app/(main)/_components/search";
import styles from "@/app/(main)/layout.module.css";
import HCard from "@/app/_components/h-card/hcard";
import { Button } from "@/components/button";
import { Row } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";
import { navigationHref } from "@/navigation";
import { Nullish } from "@/types";
import { classes } from "@/util/transforms";

/**
 * Reusable root layout.
 *
 * We need to use the root layout in our error pages (not-found.tsx, etc) but
 * those may render on client. i.e. We sometimes want to render on the client
 * but don't want to be forced to do so.
 *
 * Basically, server-side rendering can pass server state while client-side can ignore it.
 */
export default function MainLayout({
  state,
  children,
}: Readonly<{
  state?: ResponseOf<"/api/state/"> | Nullish;
  children: React.ReactNode;
}>) {
  return (
    <body className="surface-background overflow-x-hidden size-full">
      <div id="dialog_portal_container" />
      <div className="grid grid-rows-[min-content_1fr_min-content] grid-cols-1 gap-y-16 h-full items-start">
        <header
          className={classes(styles.headerGrid, "p-edge items-center gap-4")}
        >
          <h1
            className="[grid-area:title] whitespace-nowrap font-normal justify-self-start"
            id="top"
          >
            <Link href={navigationHref("home")} className="no-underline">
              {process.env.NEXT_PUBLIC_SITE_NAME}
            </Link>
          </h1>

          <GlobalSearch containerClassName="[grid-area:search]" />
          <Row className="[grid-area:toolbar] gap-4 justify-self-end justify-end">
            <ThemeController />
            <Button href={navigationHref("about")}>About</Button>
            <Button href={navigationHref("contact")}>Contact</Button>
          </Row>

          <GlobalMotd
            motd={state?.motd}
            className="[grid-area:motd] readable justify-self-center"
          />
        </header>

        {children}

        <footer className="mx-auto pb-8">
          <HCard hcard={state?.hcard} showDetail={false} className="hidden!" />
          <ReturnToTopButton />
        </footer>
      </div>
    </body>
  );
}
