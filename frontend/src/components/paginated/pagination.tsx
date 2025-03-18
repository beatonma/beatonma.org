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
  reset: () => Promise<void>;
  href: AdjacentPages;
}

export const usePagination = <P extends PathWithPagination>(
  path: P,
  init?: PagedResponseOf<P>,
  query?: Query<P> | undefined,
): Paginated<PageItemType<P>> => {
  const [items, setItems] = useState<PageItemType<P>[]>(init?.items ?? []);
  const [error, setError] = useState<any>();
  const totalItemsAvailable = useRef(init?.count ?? -1);
  const offset = useRef(init?.items?.length ?? 0);
  const [isLoading, setIsLoading] = useState(false);
  const loadingRef = useRef(false);
  const isInitialised = useRef(false);
  const [adjacentPages, setAdjacentPages] = useState<AdjacentPages>({
    next: init?.next ?? null,
    previous: init?.previous ?? null,
  });

  const reset = useCallback(async () => {
    setItems([]);
    setError(undefined);
    setIsLoading(false);
    totalItemsAvailable.current = -1;
    offset.current = 0;
    loadingRef.current = false;
  }, []);

  const loadNext = useCallback(async () => {
    if (loadingRef.current) return;
    if (
      totalItemsAvailable.current >= 0 &&
      offset.current >= totalItemsAvailable.current
    )
      return;

    loadingRef.current = true;
    setIsLoading(true);
    setError(undefined);

    try {
      const fullQuery: Query<P> = {
        ...((query ?? {}) as Query<P>),
        offset: offset.current,
      };
      const {
        data,
        error: err,
        response,
      } = await getPaginated(path, fullQuery);

      if (err || !data) {
        console.error(err);
        setError(err);
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
      setError(e);
    } finally {
      setIsLoading(false);
      loadingRef.current = false;
    }
  }, [path, query]);

  useEffect(() => {
    if (isInitialised.current) {
      void reset().then(loadNext);
    } else if (!init) {
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
