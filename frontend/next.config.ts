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

  webpack(config) {
    /** Configuration to enable importing SVG files as React components via @svgr/webpack.*/
    // Grab the existing rule that handles SVG imports
    const fileLoaderRule = config.module.rules.find((rule: any) =>
      rule.test?.test?.(".svg"),
    );

    config.module.rules.push(
      // Reapply the existing rule, but only for svg imports ending in ?url
      {
        ...fileLoaderRule,
        test: /\.svg$/i,
        resourceQuery: /url/, // *.svg?url
      },
      // Convert all other *.svg imports to React components
      {
        test: /\.svg$/i,
        issuer: fileLoaderRule.issuer,
        resourceQuery: { not: [...fileLoaderRule.resourceQuery.not, /url/] }, // exclude if *.svg?url
        use: [{ loader: "@svgr/webpack", options: { icon: true } }],
      },
    );

    // Modify the file loader rule to ignore *.svg, since we have it handled now.
    fileLoaderRule.exclude = /\.svg$/i;

    return config;
  },
};

export default nextConfig;
