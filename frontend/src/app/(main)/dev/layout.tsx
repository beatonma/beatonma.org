import { InlineButton } from "@/components/button";
import { Row, Separator } from "@/components/layout";
import { ThemeController } from "@/features/themed";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Row className="gap-4 justify-end p-edge max-w-full overflow-x-auto *:shrink-0">
        <InlineButton href="/dev/">Components</InlineButton>
        <Separator />
        <InlineButton href="/dev/main/">Main layout</InlineButton>
        <InlineButton href="/dev/search/">Search</InlineButton>
        <InlineButton href="/dev/media/">Media</InlineButton>
        <Separator />
        <ThemeController />
      </Row>
      <div className="readable mx-auto space-y-16 mb-16">{children}</div>
    </>
  );
}
