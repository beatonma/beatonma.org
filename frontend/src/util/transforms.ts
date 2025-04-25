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

/*
    (rf"{_URL_PREFIX}(?:old\.)?reddit\.com/r/{_NAME}.*", r"/r/\g<name>"),
    (rf"{_URL_PREFIX}(?:old\.)?reddit\.com/u(?:ser)?/{_NAME}.*", r"/u/\g<name>"),
    (rf"{_URL_PREFIX}github\.com/{_NAME}.*", r"github/\g<name>"),
    (rf"{_URL_PREFIX}pypi\.org/project/{_NAME}.*", r"pypi/\g<name>"),
    (rf"{_URL_PREFIX}thingiverse\.com/thing:(?P<name>\d+).*", r"thingiverse/\g<name>"),
    (rf"{_URL_PREFIX}youtube\.com/watch\?v={_NAME}.*", r"youtube"),
    (rf"{_URL_PREFIX}youtube\.com/{_NAME}.*", r"youtube/\g<name>"),
*/

const simpleUrl = (
  url: URL,
  pathPattern: RegExp,
  replace: (value: string) => string,
) => url.pathname.match(pathPattern)?.map(replace)?.[0];
const FancyUrl: Record<string, (url: URL) => string | undefined> = {
  "github.com": (url) =>
    simpleUrl(url, /@?([-\w]+)\/?$/, (name) => `github.com/${name}`),
  // url.pathname.match(/@?([-\w]+)\/?$/)?.map((name) => `github/${name}`)[0],
  "youtube.com": (url) =>
    url.pathname.match(/@?([-\w]+)\/?$/)?.map((name) => `youtube/${name}`)[0],
  "reddit.com": (url) =>
    url.pathname
      .match(/u(?:ser)?\/([-\w]+)\/?$/)
      ?.map((name) => `u/${name}`)[0] ??
    url.pathname.match(/r\/([-\w]+)\/?$/)?.map((name) => `r/${name}`)[0],
  "pypi.org": (url) =>
    simpleUrl(url, /project\/(\w})/, (name) => `pypi/${name}`),
};

export type UrlFormatStyle = "default" | "brand";
export const formatUrl = (
  url: string | URL | Nullish,
  style?: UrlFormatStyle,
): string => {
  if (!url) return "";
  try {
    const _url = new URL(url as string | URL);

    // if (ProfileUrl.includes(_url.hostname)) {
    //   const profileUrl = _url.pathname
    //     .match(/@?([-\w]+)/)
    //     ?.map(
    //       (it) => `${_url.hostname.replace(/\.(com|org)$/, "")}/${it}`,
    //     )?.[1];
    //   if (profileUrl) return profileUrl;
    // }
    const simpleHostName = _url.hostname.replace(/^((www|old)\.)/, "");

    if (style === "brand") {
      return simpleHostName.replace(/\.(com|org)$/, "");
    }

    return FancyUrl[simpleHostName]?.(_url) ?? simpleHostName;
  } catch (e) {
    return "__BAD_URL__";
  }
};
