import { int } from "@/components/number";

/**
 * [Single: ZeroOrMany]
 */
const Plurals = {
  result: ["result", "results"],
  mention: ["mention", "mentions"],
  change: ["change", "changes"],
  repository: ["repository", "repositories"],
  hour: ["hour", "hours"],
  minute: ["minute", "minutes"],
  second: ["second", "seconds"],
};

export const plural = (
  key: keyof typeof Plurals | [string, string],
  count: number,
  format?: (pluralized: string) => string,
) => {
  const index = count === 1 ? 0 : 1;

  const word = (typeof key === "string" ? Plurals[key] : key)[index];

  if (format) {
    return format(word);
  }

  return `${int(count)} ${word}`;
};
