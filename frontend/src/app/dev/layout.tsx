import { InlineButton } from "@/components/button";
import { Row, Separator } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Row className="gap-4 justify-end p-edge">
        <InlineButton href="/dev/">Base</InlineButton>
        <InlineButton href="/dev/media/">Media</InlineButton>
        <Separator />
        <ThemeController />
      </Row>
      <div className="readable mx-auto space-y-16 mb-16">{children}</div>
    </>
  );
}
