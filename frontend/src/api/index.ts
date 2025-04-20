import { notFound } from "next/navigation";
import createClient from "openapi-fetch";
import { PathsWithMethod } from "openapi-typescript-helpers";
import type { components, paths } from "./api";

export type schemas = components["schemas"];

export interface Paged<T> {
  items: T[];
  count: number;
  page_size: number;
  next: number | null;
  previous: number | null;
}
export type ApiResponse<T> =
  | {
      data: T;
      error?: never;
      response: Response;
    }
  | {
      data?: never;
      error: unknown;
      response: Response;
    };
type ApiPromise<T> = Promise<ApiResponse<T>>;

type Path = keyof paths;

type GetResponse200<T> = { get: { responses: { 200: T } } };
type GetResponse200Json<T> = GetResponse200<{
  content: { "application/json": T };
}>;

/** Return the union of all paths which extend T. */
type PathsOf<T> = {
  [Path in keyof paths]: paths[Path] extends T ? Path : never;
}[keyof paths];

/** Return the type of the JSON data returned by the given path. */
export type ResponseOf<P extends Path> =
  paths[P] extends GetResponse200Json<infer JSON> ? JSON : never;

/** Return the type of items in the paginated response of the given path. */
export type PageItemType<P extends PathWithPagination> =
  paths[P] extends GetResponse200Json<Paged<infer ItemType>> ? ItemType : never;

export type PagedResponseOf<P extends PathWithPagination> =
  paths[P] extends GetResponse200Json<Paged<unknown>>
    ? Paged<PageItemType<P>>
    : never;

type PathWithSlug = PathsOf<{
  get: {
    parameters: {
      path: {
        slug: string;
      };
    };
  };
}>;

type PathWithGetResponse200Json<T> = PathsOf<GetResponse200Json<T>>;

/** Paths which return a response of Paged<T> */
export type PathWithPaginationOf<T> = PathWithGetResponse200Json<Paged<T>>;

/** Paths which returns a Paged response of any kind.*/
export type PathWithPagination = PathWithPaginationOf<unknown>;

/**
 * Paths which accept a ?query=string parameter.
 */
type PathWithSearch = {
  [Path in keyof paths]: paths[Path] extends {
    get: {
      parameters: infer Parameters;
    };
  }
    ? Parameters extends { query?: never }
      ? never
      : Parameters extends { query?: { query?: string } }
        ? Path
        : never
    : never;
}[keyof paths];

export type SearchablePath = PathWithPagination & PathWithSearch;

export const client = createClient<paths>({
  baseUrl: process.env.API_BASE_URL,
});

type PathWithGet = PathsWithMethod<paths, "get">;
type Params<P extends PathWithGet> = paths[P]["get"]["parameters"];
export type Query<P extends PathWithGet> =
  paths[P]["get"]["parameters"]["query"];

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
