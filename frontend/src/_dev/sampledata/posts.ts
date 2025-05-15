import { PostPreview } from "@/api/types";

const choose = <T>(options: T[]): T =>
  options[Math.floor(options.length * Math.random())];

const anyString = () => Math.random().toString(36).slice(2, 7);

export const generatePostPreview = (): PostPreview => ({
  post_type: choose(["app", "changelog", "post"]),
  title: anyString(),
  url: anyString(),
  is_published: true,
  published_at: "2023-05-27T15:12:48Z",
  theme: null,
  hero_embedded_url: null,
  hero_image: null,
  content_html: anyString(),
  content_script: null,
  files: [],
  is_preview: true,
});

export const generatePostPreviews = (n: number): PostPreview[] =>
  [...Array(n).keys()].map(() => generatePostPreview());
