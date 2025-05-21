import { notFound } from "next/navigation";
import createClient from "openapi-fetch";
import type { paths } from "@/api/api";
import type {
  ApiPromise,
  PagedResponseOf,
  Params,
  PathWithGet,
  PathWithPagination,
  PathWithSlug,
} from "./types";

export const client = createClient<paths>({
  baseUrl: process.env.API_BASE_URL,
});

const get = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) =>
  client.GET(
    path,
    // @ts-expect-error Unable to find 'correct' type for this object
    {
      params,
      signal,
    },
  );

export const getOrNull = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) => {
  const response = await get(path, params, signal);
  const data = response.data;

  return data ?? null;
};

export const getOr404 = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) => {
  const data = await getOrNull(path, params, signal);

  if (!data) return notFound();
  return data;
};

export const getOrThrow = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) => {
  const response = await get(path, params, signal);
  const { data, error } = response;

  if (!data) throw new Error(`Failed to load data from ${path}: ${error}`);
  return data;
};

type Slug = string | string[] | undefined;
export const resolveSlug = async (
  slug: Slug | Promise<{ slug: Slug }>,
): Promise<string | undefined> => {
  const value = await slug;
  let _slug: Slug;
  if (typeof value === "object" && !Array.isArray(value)) {
    _slug = value.slug;
  } else {
    _slug = value;
  }

  if (Array.isArray(_slug)) _slug = _slug.join("/");
  return _slug || undefined;
};
export const getSlug = async <P extends PathWithSlug>(
  path: P,
  slug: Slug | Promise<{ slug: Slug }>,
  signal?: AbortSignal,
) => {
  const resolved = await resolveSlug(slug);
  if (!resolved) return notFound();

  return getOr404(path, { path: { slug: resolved } }, signal);
};

export const getPaginated = <P extends PathWithPagination>(
  path: P,
  query: Params<P>,
  signal?: AbortSignal,
): ApiPromise<PagedResponseOf<P>> => {
  return get(path, query, signal) as ApiPromise<PagedResponseOf<P>>;
};
