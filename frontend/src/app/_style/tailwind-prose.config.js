const mix = (one, two, percent = 50) => {
  return `color-mix(in srgb, var(${one}) ${percent}%, var(${two}))`;
};

const light = (variant) => `var(--color-stone-${variant})`;
const dark = (variant) => `var(--color-slate-${variant})`;

const vibrant = (percent) =>
  percent ? mix("--vibrant", "--bg", percent) : "var(--vibrant)";
const muted = (percent) =>
  percent ? mix("--muted", "--bg", percent) : "var(--muted)";

const themes = {
  body: [light(800), dark(200)],
  headings: [light(900), dark(100)],
  lead: [light(700), dark(300)],
  links: [light(950), dark(100)],
  bold: [light(900), dark(100)],
  counters: [light(700), dark(300)],
  bullets: [vibrant(), vibrant()],
  hr: [vibrant(), vibrant()],
  quotes: [light(900), dark(100)],
  "quote-borders": [vibrant(), vibrant()],
  captions: [light(600), dark(300)],
  code: [light(900), dark(100)],
  "pre-code": [light(100), dark(100)],
  "pre-bg": [light(900), muted(10)],
  "th-borders": [vibrant(80), vibrant(80)],
  "td-borders": [light(300), dark(800)],
};

const themesCss = Object.fromEntries(
  Object.entries(themes).flatMap(([key, [light, dark]]) => [
    [`--tw-prose-${key}`, light],
    [`--tw-prose-invert-${key}`, dark],
  ]),
);

/** @type {import("tailwindcss").Config} */
module.exports = {
  theme: {
    extend: {
      typography: () => ({
        DEFAULT: {
          css: {
            ...themesCss,
            a: {
              textDecoration: "no-underline",
            },
            "a:hover": {
              textDecoration: "underline",
            },
          },
        },
      }),
    },
  },
};
