import { notFound } from "next/navigation";
import createClient, { FetchOptions } from "openapi-fetch";
import { FilterKeys } from "openapi-typescript-helpers";
import type { components, paths } from "./api";

export const client = createClient<paths>({
  baseUrl: process.env.API_BASE_URL,
  fetch: (original) => {
    // TODO remove: dev only
    if (typeof window !== "undefined") {
      const url = new URL(original.url);
      url.port = "80";
      const altered = new Request(url, original);
      return fetch(altered);
    }
    return fetch(original);
  },
});

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

export type Path = keyof paths;

export type Query<P extends PathWithGet> =
  paths[P]["get"]["parameters"]["query"] extends never
    ? never
    : paths[P]["get"]["parameters"]["query"];

export type PathArgs<P extends PathWithGet> =
  paths[P]["get"]["parameters"]["path"] extends never
    ? never
    : paths[P]["get"]["parameters"]["path"];

type GetInit<Path extends keyof paths> = FetchOptions<
  FilterKeys<paths[Path], "get">
>;
export const get = <P extends PathWithGet>(
  path: P,
  params?: { path?: PathArgs<P>; query?: Query<P> },
): ApiPromise<ResponseOf<P>> =>
  client.GET(path, {
    params: params,
  } as GetInit<P>) as ApiPromise<ResponseOf<P>>;

export const getSlug = async <P extends PathWithSlug>(
  path: P,
  slug: string | Promise<{ slug: string }>,
) => {
  const resolvedSlug = typeof slug === "string" ? slug : (await slug).slug;

  const response = await client.GET(path, {
    params: {
      path: {
        slug: resolvedSlug,
      },
    },
  } as GetInit<P>);

  const data = response.data;

  if (!data) return notFound();
  return data;
};

export const getPaginated = <P extends PathWithPagination>(
  path: P,
  query: Query<P>,
): ApiPromise<PagedResponseOf<P>> =>
  client.GET(path, {
    params: {
      query: query,
    },
  } as GetInit<P>) as ApiPromise<PagedResponseOf<P>>;

export type ResponseOf<P extends Path> = paths[P] extends {
  get: {
    responses: {
      200: {
        content: {
          "application/json": infer JSON;
        };
      };
    };
  };
}
  ? JSON
  : never;

export type PagedResponseOf<P extends PathWithPagination> = paths[P] extends {
  get: {
    responses: {
      200: {
        content: {
          "application/json": Paged<unknown>;
        };
      };
    };
  };
}
  ? Paged<PageItemType<P>>
  : never;

export type PageItemType<P extends PathWithPagination> =
  paths[P]["get"]["responses"][200]["content"]["application/json"] extends {
    items: (infer ItemType)[];
  }
    ? ItemType
    : never;

export type PathWithGet = {
  [Path in keyof paths]: paths[Path] extends {
    get: unknown;
  }
    ? Path
    : never;
}[keyof paths];

type PathWithSlug = {
  [Path in keyof paths]: paths[Path] extends {
    get: {
      parameters: {
        path: {
          slug: string;
        };
      };
    };
  }
    ? Path
    : never;
}[keyof paths];

/**
 * Paths which returns a Paged response.
 */
export type PathWithPagination = {
  [Path in keyof paths]: paths[Path] extends {
    get: {
      responses: {
        200: {
          content: {
            "application/json": Paged<unknown>;
          };
        };
      };
    };
  }
    ? Path
    : never;
}[keyof paths];

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
