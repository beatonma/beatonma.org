import { notFound } from "next/navigation";
import * as sdk from "@/api/client";
import {
  NetworkResult,
  getDataOr404,
  getDataOrNull,
  getDataOrThrow,
} from "@/repository/result";
import type {
  AboutDetail,
  AppDetail,
  ChangelogDetail,
  ContactForm,
  FeedQuery,
  GithubRecentEvents,
  GlobalState,
  Paginated,
  PostDetail,
  PostPreview,
  Redirect,
  TagDetail,
  WebmentionTesterSchema,
} from "@/repository/types";

type SimpleSlug = string | string[] | undefined;
export type SlugParams = { params: Promise<{ slug: SimpleSlug }> };
type Slug = SimpleSlug | Promise<{ slug: SimpleSlug }> | SlugParams;
type ResolvedSlug = string | undefined;
const resolveSlug = async (slug: Slug): Promise<ResolvedSlug> => {
  let value = await slug;
  let _slug: Slug;
  if (typeof value === "object" && !Array.isArray(value)) {
    if ("params" in value) {
      _slug = (await value.params).slug;
    } else {
      _slug = value.slug;
    }
  } else {
    _slug = value;
  }
  if (Array.isArray(_slug)) _slug = _slug.join("/");
  return _slug || undefined;
};

const resolveSlugOr404 = async (slug: Slug): Promise<string> => {
  const _slug = await resolveSlug(slug);
  if (_slug) return _slug;
  return notFound();
};

const getGlobalState: (
  signal?: AbortSignal,
) => Promise<GlobalState | null> = async (signal) => {
  const response = await sdk.mainApiGlobalStateGetGlobalState({ signal });

  return getDataOrNull<GlobalState>(response);
};

const getPaginatedPosts: (
  query: FeedQuery,
  signal?: AbortSignal,
) => Promise<NetworkResult<Paginated<PostPreview>>> = async (query, signal) => {
  return await sdk.mainApiPostsPostFeed({ query, signal });
};

const getGithubRecent: (
  signal?: AbortSignal,
) => Promise<GithubRecentEvents | null> = async (signal) => {
  const response = await sdk.githubApiGetGithubEvents({ signal });

  return getDataOrNull<GithubRecentEvents>(response);
};

const getWebmentionsTester: (
  urlPath: string,
  signal?: AbortSignal,
) => Promise<WebmentionTesterSchema> = async (urlPath, signal) => {
  const response = await sdk.webmentionsTesterApiGetTemporaryWebmentions({
    query: {
      url_path: urlPath,
    },
    signal,
  });

  return getDataOrThrow<WebmentionTesterSchema>(
    response,
    "getWebmentionsTester",
  );
};

const getApp: (slug: Slug, signal?: AbortSignal) => Promise<AppDetail> = async (
  slug,
  signal,
) => {
  const _slug = await resolveSlugOr404(slug);
  const response = await sdk.mainApiPostsApp({ path: { slug: _slug }, signal });

  return getDataOr404<AppDetail>(response);
};

const getChangelog: (
  slug: Slug,
  signal?: AbortSignal,
) => Promise<ChangelogDetail> = async (slug, signal) => {
  const _slug = await resolveSlugOr404(slug);
  const response = await sdk.mainApiPostsChangelog({
    path: { slug: _slug },
    signal,
  });

  return getDataOr404<ChangelogDetail>(response);
};

const getPost: (
  slug: Slug,
  signal?: AbortSignal,
) => Promise<PostDetail> = async (slug, signal) => {
  const _slug = await resolveSlugOr404(slug);
  const response = await sdk.mainApiPostsPost({
    path: { slug: _slug },
    signal,
  });

  return getDataOr404<PostDetail>(response);
};

const getAboutPage: (
  slug: Slug,
  signal?: AbortSignal,
) => Promise<AboutDetail> = async (slug, signal) => {
  const resolvedSlug = await resolveSlug(slug);
  const response = await (resolvedSlug
    ? sdk.mainApiPostsAbout({ path: { path: resolvedSlug }, signal })
    : sdk.mainApiPostsAboutRoot());

  return getDataOr404<AboutDetail>(response);
};

const getTags: (
  signal?: AbortSignal,
) => Promise<Array<TagDetail> | null> = async (signal) => {
  const response = await sdk.mainApiTagsTags({ signal });

  return getDataOrNull<Array<TagDetail>>(response);
};

const contact = async (form: ContactForm, signal?: AbortSignal) => {
  const response = await sdk.contactApiSendMail({ body: form, signal });

  return getDataOrNull<never>(response);
};

const redirect: (
  path: string,
  signal?: AbortSignal,
) => Promise<string> = async (path, signal) => {
  const response = await sdk.mainApiStatusCheckRedirect({
    query: { path },
    signal,
  });

  const data = await getDataOrThrow<Redirect>(response, "redirect");
  return data.redirect;
};

const Repository = {
  posts: {
    getPaginatedPosts,
    getApp,
    getAboutPage,
    getChangelog,
    getPost,
  },
  getTags,
  getGlobalState,
  getGithubRecent,
  getWebmentionsTester,
  contact,
  redirect,
};
export default Repository;
