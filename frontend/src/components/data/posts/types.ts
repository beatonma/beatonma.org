import { schemas } from "@/api";

export type PostPreview = schemas["PostPreview"];
export type AppPreview = schemas["AppPreview"];

export type PostDetail = schemas["PostDetail"];
export type AppDetail = schemas["AppDetail"];
export type ChangelogDetail = schemas["ChangelogDetail"];

export const isApp = (
  post: PostDetail | AppDetail | ChangelogDetail,
): post is AppDetail => post.post_type === "app";
export const isChangelog = (
  post: PostDetail | AppDetail | ChangelogDetail,
): post is ChangelogDetail => post.post_type === "changelog";

export type Post = PostPreview | PostDetail | AppDetail | ChangelogDetail;
