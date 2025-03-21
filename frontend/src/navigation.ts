type SearchParams = Record<string, string | number>;

const Navigation = {
  home: () => "/",
  contact: () => `/contact/`,
  post: (slug: string) => `/posts/${slug}/`,
  posts: (params?: SearchParams) => `/${searchParams(params)}`,
  tag: (tag: string) => `/tag/${tag}/`,
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

const searchParams = (params: SearchParams | undefined) => {
  if (!params) return "";

  const formatted = Object.entries(params).map(
    ([key, value]) => `${key}=${value}`,
  );
  return `?${formatted}`;
};
