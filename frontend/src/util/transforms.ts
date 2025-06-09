import { Nullish } from "@/types";

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
