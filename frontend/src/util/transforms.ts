import { MaybeString, Nullish } from "@/types";

export const classes = (...classNames: (string | undefined | null)[]) =>
  classNames.filter(Boolean).join(" ") || undefined;

/**
 * Returns a copy of props with extraClasses appended to its className attribute.
 */
export const addClass = <T extends { className?: string }>(
  props: T,
  ...extraClasses: (string | Nullish)[]
) => ({
  ...props,
  className: classes(props.className, ...extraClasses),
});

export const capitalize = (value: MaybeString | null): string | null =>
  value ? value.slice(0, 1).toUpperCase() + value.slice(1) : null;

export const formatUrl = (url: string): string => {
  const _url = new URL(url);
  return _url.hostname.replace("www.", "");
};
