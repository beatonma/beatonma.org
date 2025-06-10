import { Nullish } from "@/types";

export const capitalize = (value: string | Nullish): string | null =>
  value ? value.slice(0, 1).toUpperCase() + value.slice(1) : null;

/** When given an HTML string, returns the plain text content from the first element. */
export const getPlaintextSummaryFromHtml = (maybeHtml: string) => {
  // Strip any external html tags
  const html = maybeHtml.replace(/.*?<(\w+).*?>(.*?)<\/\1>.*/, "$2");

  // Strip any remaining tags from the content.
  return html
    .replaceAll(/<(\w+).*?>(.*?)<\/\1>/g, "$2") // Normal elements
    .replaceAll(/<(.*?)\/>/g, "") // Remove <self-closing />
    .replaceAll(/<!--(.*?)-->/g, "") // Remove <!-- comments -->
    .trim();
};
