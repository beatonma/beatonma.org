import { ReactNode } from "react";
import { GlobalState } from "@/api/types";
import { GlobalHCard } from "@/app/_components/h-card";
import { Button } from "@/components/button";
import { Row } from "@/components/layout";
import { ThemeController } from "@/features/themed";
import { navigationHref } from "@/navigation";
import { Nullish } from "@/types";
import { classes } from "@/util/transforms";
import styles from "./main-layout.module.css";
import { GlobalMotd } from "./motd";
import { ReturnToTopButton } from "./return-to-top";
import { GlobalSearch } from "./search";

export const MainLayout = ({
  state,
  children,
}: Readonly<{
  state?: GlobalState | Nullish;
  children: ReactNode;
}>) => (
  <body className="surface-background overflow-x-hidden size-full">
    <div id="dialog_portal_container" />
    <div className="grid grid-rows-[min-content_1fr_min-content] grid-cols-1 gap-y-8 h-full items-start">
      <header
        className={classes(styles.headerGrid, "p-edge items-center gap-4")}
      >
        <h1
          className="[grid-area:title] whitespace-nowrap font-normal justify-self-start"
          id="top"
        >
          <a href={navigationHref("home")} className="no-underline">
            {process.env.NEXT_PUBLIC_SITE_NAME}
          </a>
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
        <GlobalHCard
          hcard={state?.hcard}
          showDetail={false}
          className="hidden!"
        />
        <ReturnToTopButton />
      </footer>
    </div>
  </body>
);
