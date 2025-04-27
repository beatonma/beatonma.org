import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#111111",
};
export const metadata: Metadata = {
  title: {
    default: process.env.NEXT_PUBLIC_SITE_NAME,
    template: `%s - ${process.env.NEXT_PUBLIC_SITE_NAME}`,
  },
  description: process.env.NEXT_PUBLIC_SITE_NAME,
  alternates: {
    canonical: "/",
    types: {
      "application/rss+xml": [{ url: "/feed/", title: "" }],
    },
  },
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
