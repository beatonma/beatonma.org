import type { components } from "@/api/api";
import type { paths } from "./api";

type schemas = components["schemas"];
export type Path = keyof paths;
export type { Query, Paged } from "./client/types";

// Common
export type GlobalState = schemas["GlobalState"];

// Posts
export type PostPreview = schemas["PostPreview"];
export type AppPreview = schemas["AppPreview"];
export type PostDetail = schemas["PostDetail"];
export type AppDetail = schemas["AppDetail"];
export type ChangelogDetail = schemas["ChangelogDetail"];
export type AboutDetail = schemas["AboutDetail"];

export type PreviewPost = PostPreview | AppPreview;
export type DetailedPost =
  | PostDetail
  | AppDetail
  | ChangelogDetail
  | AboutDetail;

export type Theme = schemas["Theme"];
export type MediaFile = schemas["File"];

export const isApp = (post: DetailedPost): post is AppDetail =>
  post.post_type === "app";

export const isChangelog = (post: DetailedPost): post is ChangelogDetail =>
  post.post_type === "changelog";

// Github
export type GithubRecentEvents = schemas["GithubRecentEvents"];
export type GithubPrivateEvent = schemas["GithubPrivateEvent"];
export type GithubCreatePayload = schemas["GithubPublicCreateEvent"]["payload"];
export type GithubPushPayload =
  schemas["GithubPublicPushEvent"]["payload"][number];
export type GithubPullRequestPayload =
  schemas["GithubPublicPullRequestEvent"]["payload"];
export type GithubIssuePayload = schemas["GithubPublicIssueEvent"]["payload"];
export type GithubWikiPayload =
  schemas["GithubPublicWikiEvent"]["payload"][number];
export type GithubReleasePayload =
  schemas["GithubPublicReleaseEvent"]["payload"];

// Webmentions
export type Webmention = schemas["Mention"];
export type WebmentionTester = schemas["WebmentionTesterSchema"];
