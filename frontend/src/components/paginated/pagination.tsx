"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  PageItemType,
  PagedResponseOf,
  type PathWithPagination,
  type Query,
  getPaginated,
} from "@/api";

interface AdjacentPages {
  next: number | null;
  previous: number | null;
}
export interface Paginated<T> {
  items: T[];
  availableItems: number;
  isLoading: boolean;
  hasMore: boolean;
  loadNext: (() => Promise<void>) | undefined;
  error: any | undefined;
  reset: (reason?: string) => Promise<void>;
  href: AdjacentPages;
}

interface PaginationConfig<P extends PathWithPagination> {
  load?: boolean;
  init?: PagedResponseOf<P>;
  query?: Query<P> | undefined;
}

export const usePagination = <P extends PathWithPagination>(
  path: P,
  config?: PaginationConfig<P>,
): Paginated<PageItemType<P>> => {
  const [items, setItems] = useState<PageItemType<P>[]>(
    config?.init?.items ?? [],
  );
  const totalItemsAvailable = useRef(config?.init?.count ?? -1);
  const offset = useRef(config?.init?.items?.length ?? 0);
  const isInitialised = useRef(false);
  const [adjacentPages, setAdjacentPages] = useState<AdjacentPages>({
    next: config?.init?.next ?? null,
    previous: config?.init?.previous ?? null,
  });
  const [isLoading, _setIsLoading] = useState(false);
  const loadingRef = useRef(false);
  const [error, _setError] = useState<any>();
  const errorRef = useRef(false);
  const abortController = useRef<AbortController>(null);

  const setIsLoading = useCallback((value: boolean) => {
    loadingRef.current = value;
    _setIsLoading(value);
  }, []);
  const setError = useCallback((value: unknown) => {
    errorRef.current = !!value;
    _setError(value);
  }, []);

  const reset = useCallback(async (reason?: string) => {
    abortController.current?.abort(reason ?? "Pagination reset");
    abortController.current = null;
    setItems([]);
    setError(undefined);
    setIsLoading(false);
    totalItemsAvailable.current = -1;
    offset.current = 0;
  }, []);

  const loadNext = useCallback(async () => {
    if (!(config?.load ?? true)) return;
    if (loadingRef.current || errorRef.current) return;
    if (
      totalItemsAvailable.current >= 0 &&
      offset.current >= totalItemsAvailable.current
    ) {
      return;
    }
    setIsLoading(true);
    abortController.current = new AbortController();

    try {
      const fullQuery: Query<P> = {
        ...((config?.query ?? {}) as Query<P>),
        offset: offset.current,
      };
      const {
        data,
        error: err,
        response,
      } = await getPaginated(
        path,
        { query: fullQuery },
        abortController.current?.signal,
      );

      if (err || !data) {
        console.error(err);
        setError(`${response.status}: ${response.url}`);
        return;
      }

      setAdjacentPages({
        next: data.next,
        previous: data.previous,
      });
      setItems((prev) => [...prev, ...data.items]);
      totalItemsAvailable.current = data.count;
      offset.current = offset.current + data.items.length;
    } catch (e: unknown) {
      if (e instanceof Error && e?.name === "AbortError") return;

      setError(e);
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }, [path, config?.query, config?.load]);

  useEffect(() => {
    if (isInitialised.current) {
      void reset().then(loadNext);
    } else if (!config?.init) {
      void loadNext();
    }
    isInitialised.current = true;
  }, [loadNext]);

  return {
    items: items,
    availableItems: totalItemsAvailable.current,
    isLoading: isLoading,
    error: error,
    reset: reset,
    loadNext: loadNext,
    hasMore: offset.current < totalItemsAvailable.current,
    href: adjacentPages,
  };
};
