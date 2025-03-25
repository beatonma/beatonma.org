import Link from "next/link";
import { Button } from "@/components/button";
import { Row, Separator } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";
import { navigationHref } from "@/navigation";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="grid grid-rows-[min-content_1fr_min-content] grid-cols-1 h-full items-start">
      <header className="p-edge max-xl:mb-16">
        <Row className="gap-8 justify-between flex-wrap">
          <h1 className="line-clamp-1">
            <Link href={navigationHref("home")}>{process.env.SITE_NAME}</Link>
          </h1>

          <Row className="gap-4">
            <Button icon="Dev" href="/dev/">
              Components
            </Button>
            <Separator />
            <Button href={navigationHref("contact")}>Contact</Button>
            <ThemeController />
          </Row>
        </Row>
      </header>

      {children}

      <footer></footer>
    </div>
  );
}
