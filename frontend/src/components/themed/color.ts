import { MaybeString, Nullish } from "@/types";

type ThreeChannel = [number, number, number];

const WcagContrast = 8; // https://www.w3.org/TR/WCAG21/#contrast-minimum

export const getOnColor = (
  backgroundColor: MaybeString,
  foregroundColor?: MaybeString,
  element?: HTMLElement | Nullish,
): MaybeString => {
  if (!backgroundColor) return undefined;

  const resolvedBg = resolveToRgb(backgroundColor, element);
  const resolvedFg = resolveToRgb(foregroundColor ?? backgroundColor, element);
  if (!resolvedBg || !resolvedFg) {
    return undefined;
  }

  const [r, g, b] = adjustForegroundContrast(resolvedBg, resolvedFg);
  return `rgb(${r}, ${g}, ${b})`;
};

const resolveToRgb = (
  color: MaybeString,
  element?: HTMLElement | Nullish,
): ThreeChannel | undefined => {
  if (!color) return undefined;

  if (color.includes("--")) {
    const cssName = color.match(/var\((--[^)\s]+)\)/)?.[1];
    if (!cssName) return undefined;

    return resolveToRgb(
      (element ?? document.body).computedStyleMap().get(cssName)?.toString(),
    );
  }

  return rgbToRgb(color) ?? hexToRgb(color);
};

const adjustForegroundContrast = (
  background: ThreeChannel,
  foreground: ThreeChannel,
): ThreeChannel => {
  const backgroundLuminance = getLuminance(background);

  const step = 5;

  // Try and find a suitable contrast by adjusting towards black
  let adjusted: ThreeChannel = [...foreground];
  // console.log(`original: ${adjusted}`);
  // if (
  //   adjust(backgroundLuminance, adjusted, (it) => Math.max(0, it - step), 0)
  // ) {
  //   console.log(`towards black: ${adjusted}`);
  //   return adjusted;
  // }
  //
  // // Try and find a suitable contrast by adjusting towards white
  // adjusted = [...foreground];
  // adjust(backgroundLuminance, adjusted, (it) => Math.min(255, it + step), 255);
  // console.log(`towards white: ${adjusted}`);
  // return adjusted;

  for (let i = 0; i < 100; i++) {
    if (
      getContrastRatio(backgroundLuminance, getLuminance(adjusted)) >
      WcagContrast
    ) {
      return adjusted;
    }

    if (adjusted.every((it) => it === 0)) {
      // Already reached black. Try going the other direction instead.
      break;
    }

    const [r, g, b] = adjusted;

    adjusted = [
      Math.max(0, r - step),
      Math.max(0, g - step),
      Math.max(0, b - step),
    ];
  }

  adjusted = [...foreground];
  for (let i = 0; i < 100; i++) {
    if (
      getContrastRatio(backgroundLuminance, getLuminance(adjusted)) >
      WcagContrast
    ) {
      return adjusted;
    }

    if (adjusted.every((it) => it === 255)) {
      // Already reached white
      break;
    }

    const [r, g, b] = adjusted;

    adjusted = [
      Math.min(255, r + step),
      Math.min(255, g + step),
      Math.min(255, b + step),
    ];
  }
  return adjusted;
};

const adjust = (
  backgroundLuminance: number,
  adjusted: ThreeChannel,
  _adjust: (component: number) => number,
  limit: number,
): ThreeChannel | undefined => {
  for (let i = 0; i < 100; i++) {
    if (
      getContrastRatio(backgroundLuminance, getLuminance(adjusted)) >
      WcagContrast
    ) {
      // Suitable contrast found.
      return adjusted;
    }

    if (adjusted.every((it) => it === limit)) {
      // Limit reached on all components.
      break;
    }

    adjusted[0] = _adjust(adjusted[0]);
    adjusted[1] = _adjust(adjusted[1]);
    adjusted[2] = _adjust(adjusted[2]);
  }
};

const getLuminance = (rgb: ThreeChannel): number => {
  const [r, g, b] = rgb.map((val) => {
    const sRGB = val / 255;
    return sRGB <= 0.03928
      ? sRGB / 12.92
      : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  }) as ThreeChannel;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

const getContrastRatio = (luminance1: number, luminance2: number): number => {
  const lighter = Math.max(luminance1, luminance2);
  const darker = Math.min(luminance1, luminance2);
  return (lighter + 0.05) / (darker + 0.05);
};

const rgbToRgb = (rgb: string): ThreeChannel | undefined => {
  try {
    return rgb
      .match(/^(?:rgba?\()?(\d+)[\s,]+(\d+)[\s,]+(\d+)(?:[/,\s\d.]+)?\)?$/)
      ?.slice(1)
      ?.map((it) => {
        const asNumber = parseInt(it);
        if (isNaN(asNumber))
          throw new Error(`Failed to parse color as RGB: ${rgb} ${it}`);
        return asNumber;
      }) as ThreeChannel;
  } catch (e) {
    console.debug(e);
    return undefined;
  }
};

const hexToRgb = (hex: string): ThreeChannel | undefined => {
  hex = hex.replace("#", "");

  const pattern = {
    3: /^([a-f\d])([a-f\d])([a-f\d])$/i,
    6: /^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i,
    8: /^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i,
  }[hex.length];
  if (!pattern) return undefined;

  try {
    return hex
      .match(pattern)
      ?.slice(1)
      ?.map((it) => {
        const asNumber = parseInt(it, 16);
        if (isNaN(asNumber))
          throw new Error(`Failed to convert hex to RGB: ${hex}`);
        return asNumber;
      }) as ThreeChannel;
  } catch (e) {
    console.debug(e);
    return undefined;
  }
};

export const _private = { resolveToRgb };
