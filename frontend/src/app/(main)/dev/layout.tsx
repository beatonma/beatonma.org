import { InlineButton } from "@/components/button";
import { Row, Separator } from "@/components/layout";
import { ThemeController } from "@/features/themed";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div>
      <Row scrollable className="gap-4 justify-end p-edge">
        <InlineButton href="/dev/">Components</InlineButton>
        <Separator />
        <InlineButton href="/dev/search/">Search</InlineButton>
        <InlineButton href="/dev/media/">Media</InlineButton>
        <InlineButton href="/dev/mentions/">Webmentions</InlineButton>
        <Separator />
        <ThemeController />
      </Row>
      <div className="readable mx-auto space-y-16 mb-16">{children}</div>
    </div>
  );
}
