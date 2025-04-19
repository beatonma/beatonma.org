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

export const formatUrl = (url: string | URL | Nullish): string => {
  if (!url) return "";
  try {
    const _url = new URL(url as string | URL);
    return _url.hostname.replace("www.", "");
  } catch (e) {
    return "__BAD_URL__";
  }
};
