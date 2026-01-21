import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  trailingSlash: true,
  async rewrites() {
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: "/media/:path*",
          destination: `${process.env.API_BASE_URL}/media/:path*`,
        },
      ];
    }
    return [];
  },
  async redirects() {
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: `/${process.env.ADMIN_URL}:path*`,
          destination: `${process.env.API_BASE_URL}/${process.env.ADMIN_URL}:path*`,
          permanent: false,
        },
      ];
    }
    return [];
  },
  turbopack: {
    rules: {
      "*.svg": {
        loaders: [
          {
            loader: "@svgr/webpack",
            options: {
              icon: true,
            },
          },
        ],
        as: "*.js",
      },
    },
  },
};

export default nextConfig;
