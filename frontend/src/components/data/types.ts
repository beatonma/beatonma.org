import { schemas } from "@/api";

export type PostPreview = schemas["PostPreview"];
export type AppPreview = schemas["AppPreview"];

export type PostDetail = schemas["PostDetail"];
export type AppDetail = schemas["AppDetail"];
export type ChangelogDetail = schemas["ChangelogDetail"];

export type Post = PostPreview | PostDetail | AppDetail | ChangelogDetail;

export type Webmention = schemas["Mention"];

export const isPost = (
  post: PostDetail | AppDetail | ChangelogDetail,
): post is PostDetail => post.post_type === "post";
export const isApp = (
  post: PostDetail | AppDetail | ChangelogDetail,
): post is AppDetail => post.post_type === "app";
export const isChangelog = (
  post: PostDetail | AppDetail | ChangelogDetail,
): post is ChangelogDetail => post.post_type === "changelog";

export const isAppPreview = (
  post: PostPreview | AppPreview,
): post is AppPreview => post.post_type === "app";
