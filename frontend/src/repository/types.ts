import {
  AboutDetail,
  AppDetail as ApiAppDetail,
  ChangelogDetail as ApiChangelogDetail,
  AppPreview,
  ContactForm,
  File,
  GithubPrivateEvent,
  GithubPublicCreateEvent,
  GithubPublicIssueEvent,
  GithubPublicPullRequestEvent,
  GithubPublicPushEvent,
  GithubPublicReleaseEvent,
  GithubPublicWikiEvent,
  GithubRecentEvents,
  GlobalState,
  MainApiPostsPostFeedData,
  Mention,
  PostDetail,
  PostPreview,
  RedirectSchema,
  TagDetail,
  TempMention,
  Theme,
  WebmentionTesterSchema,
} from "@/api/client";

export type {
  AboutDetail,
  AppPreview,
  ContactForm,
  File as MediaFile,
  GithubPrivateEvent,
  GithubRecentEvents,
  GlobalState,
  Mention as Webmention,
  PostDetail,
  PostPreview,
  RedirectSchema as Redirect,
  TagDetail,
  TempMention as TemporaryWebmention,
  Theme,
  WebmentionTesterSchema,
};

// Generated ApiChangelogDetail type marks post_type as optional so here we enforce it as required.
export type ChangelogDetail = ApiChangelogDetail &
  Required<Pick<ApiChangelogDetail, "post_type">>;
export type AppDetail = Omit<ApiAppDetail, "changelog"> & {
  changelog: Array<ChangelogDetail>;
};

export type PreviewPost = PostPreview | AppPreview;
export type DetailedPost =
  PostDetail | AppDetail | ChangelogDetail | AboutDetail;

// Github
export type GithubCreatePayload = GithubPublicCreateEvent["payload"];
export type GithubPushPayload = GithubPublicPushEvent["payload"][number];
export type GithubPullRequestPayload = GithubPublicPullRequestEvent["payload"];
export type GithubIssuePayload = GithubPublicIssueEvent["payload"];
export type GithubWikiPayload = GithubPublicWikiEvent["payload"][number];
export type GithubReleasePayload = GithubPublicReleaseEvent["payload"];

export interface PaginationQuery {
  limit?: number;
  offset?: number;
}

export interface Paginated<T> {
  items: Array<T>;
  count: number;
  page_size: number;
  previous: number | null;
  next: number | null;
}

export type FeedQuery = MainApiPostsPostFeedData["query"];
