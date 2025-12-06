import { describe, test } from "@jest/globals";
import { act, renderHook, waitFor } from "@testing-library/react";
import expect from "expect";
import { generatePostPreviews } from "@/_dev/sampledata/posts";
import {
  PaginationLoader,
  usePagination,
} from "@/components/hooks/paginated/pagination";

const PageSize = 5;
const data = generatePostPreviews(11);

jest.mock("./browser", () => {
  return {
    /* Prevent calls to useRouter from next/navigation during unit tests. */
    useUpdateLocationQuery: () => {
      return () => console.info("mocked: useUpdateLocationQuery");
    },
  };
});

const loader: PaginationLoader<"/api/posts/"> = async (
  path,
  params,
  signal,
) => {
  const offset = params.query?.offset ?? 0;
  const limit = params.query?.limit ?? PageSize;
  const items = data.slice(offset, offset + limit);
  const response = {};

  return {
    data: {
      items: items,
      count: data.length,
      page_size: limit,
      next: offset + limit < data.length ? offset + limit : null,
      previous: offset > 0 ? Math.max(0, offset - limit) : null,
    },
    error: undefined,
    response: response as Response,
  };
};

describe("usePagination", () => {
  test("loadNext", async () => {
    const { result } = renderHook(() =>
      usePagination("/api/posts/", undefined, loader),
    );

    await waitFor(
      () => {
        // Wait for initial page load, triggered from useEffect
        expect(result.current.items.length).toBe(5);
      },
      { timeout: 100 },
    );
    expect(result.current.items.length).toBe(5);
    expect(result.current.availableItems).toBe(11);
    expect(result.current.hasMore).toBeTruthy();
    expect(result.current.href.previous).toBeNull();
    expect(result.current.href.next).toBe(5);

    await act(async () => await result.current.loadNext!());
    expect(result.current.items.length).toBe(10);
    expect(result.current.href.previous).toBe(0);
    expect(result.current.href.next).toBe(10);

    await act(async () => await result.current.loadNext!());
    expect(result.current.items.length).toBe(11);
    expect(result.current.loadNext).toBeUndefined();
    expect(result.current.hasMore).toBeFalsy();
    expect(result.current.href.next).toBeNull();
  });

  test("With preloaded data", async () => {
    const { result } = renderHook(() =>
      usePagination(
        "/api/posts/",
        {
          init: {
            items: data.slice(0, PageSize),
            next: PageSize,
            previous: null,
            count: data.length,
            page_size: PageSize,
          },
        },
        loader,
      ),
    );

    expect(result.current.items.length).toBe(5);
    expect(result.current.availableItems).toBe(11);
    expect(result.current.hasMore).toBeTruthy();
    expect(result.current.href.previous).toBeNull();
    expect(result.current.href.next).toBe(5);

    await act(async () => await result.current.loadNext!());
    expect(result.current.items.length).toBe(10);
    expect(result.current.href.previous).toBe(0);
    expect(result.current.href.next).toBe(10);
  });

  test("With `config.load:false`", async () => {
    const { result } = renderHook(() =>
      usePagination("/api/posts/", { load: false }, loader),
    );

    // Allow useEffect initializer to run.
    await timeout(200);

    expect(result.current.items.length).toBe(0);
  });
  test("With `config.load:true`", async () => {
    const { result } = renderHook(() =>
      usePagination("/api/posts/", { load: true }, loader),
    );

    // Allow useEffect initializer to run.
    await act(async () => await timeout(200));

    expect(result.current.items.length).toBe(5);
  });
});

const timeout = (millis: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(resolve, millis);
  });
