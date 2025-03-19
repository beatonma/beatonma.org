import { CSSProperties } from "react";
import { schemas } from "@/api";
import getForegroundColor from "@/components/themed/color";
import { Nullish } from "@/types";

type Theme = schemas["Theme"];
interface Themed {
  theme?: Theme | Nullish;
}
interface ThemeCss extends CSSProperties {
  "--vibrant"?: string | Nullish;
  "--on-vibrant"?: string | Nullish;
  "--muted"?: string | Nullish;
  "--on-muted"?: string | Nullish;
}

export default function itemTheme(obj: Themed): ThemeCss {
  if (!obj.theme) return {};
  const { vibrant, muted } = obj.theme;

  return {
    "--vibrant": vibrant,
    "--on-vibrant": getForegroundColor(vibrant),
    "--muted": muted,
    "--on-muted": getForegroundColor(muted),
  };
}
