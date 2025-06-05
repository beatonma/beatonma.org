import { Query } from "@/api/types";

type PostSearchParams = Query<"/api/posts/">;

const Navigation = {
  home: () => "/",
  contact: () => "/contact/",
  about: (path?: string) => (path ? `/about/${path}` : "/about/"),
  app: (slug: string) => `/apps/${slug}/`,
  appLiveInstance: (slug: string) => `/apps/${slug}/live/`,
  changelog: (slug: string) => `/changelog/${slug}/`,
  post: (slug: string) => `/posts/${slug}/`,
  posts: (params?: PostSearchParams) => `/${searchParams(params)}`,
  feed: (params?: PostSearchParams) => `/feed/${searchParams(params)}`,
  tag: (tag: string) => Navigation.posts({ tag }),
  webmentionsTest: () => `/webmentions_tester/`,
};
type Navigable = keyof typeof Navigation;
export type NavDestination = {
  [K in Navigable]: (typeof Navigation)[K] extends () => string ? K : never;
}[Navigable];

export const navigationHref = <T extends Navigable>(
  type: T,
  ...args: Parameters<(typeof Navigation)[T]>
): string => {
  type P = (...args: Parameters<(typeof Navigation)[T]>) => string;
  return (Navigation[type] as P)(...args);
};

const searchParams = (params: Record<string, string | number> | undefined) => {
  if (!params) return "";

  const formatted = Object.entries(params)
    .filter(([key, value]) => !!value)
    .map(([key, value]) => `${key}=${value}`)
    .join("&");
  if (!formatted) return "";
  return `?${formatted}`;
};

export const absoluteUrl = (path: string | undefined): string | undefined =>
  path ? `${process.env.NEXT_PUBLIC_SITE_BASE_URL}${path}` : undefined;
