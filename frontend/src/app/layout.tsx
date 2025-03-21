import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#111111",
};
export const metadata: Metadata = {
  title: process.env.SITE_NAME,
  description: process.env.SITE_NAME,
  alternates: {
    canonical: "/",
    types: {
      "application/rss+xml": [{ url: "/feed/", title: "" }],
    },
  },
  verification: {
    google: process.env.GOOGLE_SITE_VERIFICATION,
  },
  icons: {
    // This is unhinged, but it seems to be the only way to set a 'nonstandard' link.
    other: {
      rel: "webmention",
      url: "/webmention/",
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="size-full">
      <body className="surface-background overflow-x-hidden size-full">
        <div id="dialog_portal_container" />
        {children}
      </body>
    </html>
  );
}
