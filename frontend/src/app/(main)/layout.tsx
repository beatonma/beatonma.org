import Link from "next/link";
import React from "react";
import { getOrNull } from "@/api";
import ReturnToTopButton from "@/app/(main)/_components/return-to-top";
import GlobalSearch from "@/app/(main)/_components/search";
import { Button } from "@/components/button";
import DangerousHtml from "@/components/html";
import { Row } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";
import { navigationHref } from "@/navigation";
import { classes } from "@/util/transforms";
import styles from "./layout.module.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const globalState = await getOrNull("/api/state/");

  return (
    <div className="grid grid-rows-[min-content_1fr_min-content] grid-cols-1 gap-y-16 h-full items-start">
      <header
        className={classes(styles.headerGrid, "p-edge items-center gap-4")}
      >
        <h1
          className="[grid-area:title] line-clamp-1 font-normal justify-self-start"
          id="top"
        >
          <Link href={navigationHref("home")} className="no-underline">
            {process.env.NEXT_PUBLIC_SITE_NAME}
          </Link>
        </h1>

        <Row className="[grid-area:toolbar] gap-4 justify-self-end justify-end">
          <ThemeController />
          <Button href={navigationHref("about")}>About</Button>
          <Button href={navigationHref("contact")}>Contact</Button>
        </Row>

        <GlobalSearch containerClassName="[grid-area:search]" />
      </header>

      {children}

      <footer className="mx-auto pb-8">
        <DangerousHtml html={globalState?.hcard} className="hidden h-card" />
        <ReturnToTopButton />
      </footer>
    </div>
  );
}
