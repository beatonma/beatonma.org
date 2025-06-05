import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#55c191",
};
export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_BASE_URL),
  title: {
    default: process.env.NEXT_PUBLIC_SITE_NAME,
    template: `%s - ${process.env.NEXT_PUBLIC_SITE_NAME}`,
  },
  description: process.env.NEXT_PUBLIC_SITE_NAME,
  verification: {
    google: process.env.NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION,
  },
  icons: {
    // This is unhinged, but it seems to be the only way to set a 'nonstandard' link.
    other: {
      rel: "webmention",
      url: "/api/webmention/",
    },
  },
  openGraph: {
    siteName: process.env.NEXT_PUBLIC_SITE_NAME,
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="size-full">
      {children}
    </html>
  );
}
