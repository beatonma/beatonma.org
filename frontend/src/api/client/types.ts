import { PathsWithMethod } from "openapi-typescript-helpers";
import type { paths } from "@/api/api";
import type { Path } from "@/api/types";

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
export type ApiPromise<T> = Promise<ApiResponse<T>>;

type GetResponse200<T> = { get: { responses: { 200: T } } };
type GetResponse200Json<T> = GetResponse200<{
  content: { "application/json": T };
}>;

/** Return the union of all paths which extend T. */
type PathsOf<T> = {
  [P in Path]: paths[P] extends T ? P : never;
}[Path];

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

export type PathWithSlug = PathsOf<{
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
  [P in Path]: paths[P] extends {
    get: {
      parameters: infer Parameters;
    };
  }
    ? Parameters extends { query?: never }
      ? never
      : Parameters extends { query?: { query?: string } }
        ? P
        : never
    : never;
}[Path];

export type SearchablePath = PathWithPagination & PathWithSearch;

export type PathWithGet = PathsWithMethod<paths, "get">;
export type Params<P extends PathWithGet> = paths[P]["get"]["parameters"];
export type Query<P extends PathWithGet> =
  paths[P]["get"]["parameters"]["query"];
