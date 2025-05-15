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

export const getSlug = async <P extends PathWithSlug>(
  path: P,
  slug: string | Promise<{ slug: string }>,
  signal?: AbortSignal,
) => {
  const resolvedSlug = typeof slug === "string" ? slug : (await slug).slug;

  return getOr404(path, { path: { slug: resolvedSlug } }, signal);
};

export const getPaginated = <P extends PathWithPagination>(
  path: P,
  query: Params<P>,
  signal?: AbortSignal,
): ApiPromise<PagedResponseOf<P>> => {
  return get(path, query, signal) as ApiPromise<PagedResponseOf<P>>;
};
