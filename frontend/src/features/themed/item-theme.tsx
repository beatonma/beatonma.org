import { CSSProperties } from "react";
import { Theme } from "@/api/types";
import { Nullish } from "@/types";
import { getForegroundColor } from "./color";

interface Themed {
  theme?: Theme | Nullish;
}
interface ThemeCss extends CSSProperties {
  "--vibrant"?: string | Nullish;
  "--on-vibrant"?: string | Nullish;
  "--muted"?: string | Nullish;
  "--on-muted"?: string | Nullish;
  "--hover"?: string | Nullish;
  "--selection-fg"?: string | Nullish;
  "--selection-bg"?: string | Nullish;
}

export const itemTheme = (
  obj: Theme | Themed | Nullish,
  mergeInto?: CSSProperties,
): ThemeCss => {
  const theme = isThemed(obj) ? obj.theme : obj;
  if (!theme) return mergeInto ?? {};

  const { vibrant, muted } = theme;

  return {
    "--vibrant": vibrant,
    "--on-vibrant": getForegroundColor(vibrant),
    "--muted": muted,
    "--on-muted": getForegroundColor(muted),
    "--hover": vibrant,
    "--selection-bg": vibrant,
    "--selection-fg": muted,
    ...(mergeInto ?? {}),
  } as CSSProperties;
};

const isThemed = (obj: Theme | Themed | Nullish): obj is Themed =>
  !!obj && "theme" in obj;
