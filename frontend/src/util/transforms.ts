import { MaybeString, Nullish } from "@/types";

export const joinNonEmpty = (
  separator: string = " ",
  ...parts: (string | undefined | null)[]
) => parts.filter(Boolean).join(separator) || undefined;

export const classes = (...classNames: (string | undefined | null)[]) =>
  joinNonEmpty(" ", ...classNames);

/**
 * Returns a copy of props with extraClasses appended to its className attribute.
 */
export const addClass = <T extends { className?: string }>(
  props: T,
  ...extraClasses: (string | Nullish)[]
): T => ({
  ...props,
  className: classes(props.className, ...extraClasses),
});

export const capitalize = (value: MaybeString | null): string | null =>
  value ? value.slice(0, 1).toUpperCase() + value.slice(1) : null;

export type UrlFormatStyle = "default" | "brand";
export const formatUrl = (
  url: string | URL | Nullish,
  style?: UrlFormatStyle,
): string => {
  if (!url) return "";
  try {
    const _url = new URL(url as string | URL);
    const simpleHostName = _url.hostname.replace(/^((www|old)\.)/, "");

    if (style === "brand") {
      return simpleHostName.replace(/\.(com|org)$/, "");
    }

    return FancyUrl[simpleHostName]?.(_url) ?? simpleHostName;
  } catch (e) {
    return "__BAD_URL__";
  }
};

const simpleUrl = (
  url: URL,
  pathPattern: RegExp,
  replace: (value: string) => string,
) => url.pathname.match(pathPattern)?.map(replace)?.[1];

const FancyUrl: Record<string, (url: URL) => string | undefined> = {
  "github.com": (url) => {
    const match = url.pathname.match(
      /^\/(?<name>[^#?/\s]+)(?:\/)?(?<repo>[^/]+)?.*?$/,
    );
    if (!match?.groups) return undefined;
    const { name, repo } = match.groups;

    if (repo) return `github/${repo}`;
    if (name) return `github/@${name}`;
  },

  "youtube.com": (url) =>
    url.pathname.match(/@([-\w]+)\/?$/)?.map((name) => `youtube/${name}`)[1],

  "reddit.com": (url) =>
    url.pathname
      .match(/u(?:ser)?\/([-\w]+)\/?$/)
      ?.map((name) => `u/${name}`)[1] ??
    url.pathname.match(/r\/([-\w]+)\/?$/)?.map((name) => `r/${name}`)[1],

  "pypi.org": (url) =>
    simpleUrl(url, /(?:project|user)\/([-\w]+)/, (name) => `pypi/${name}`),
};
