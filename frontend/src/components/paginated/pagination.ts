"use client";

import {
  RefObject,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { getPaginated } from "@/api";
import type {
  PageItemType,
  PagedResponseOf,
  PathWithPagination,
  Query,
} from "@/api/client/types";

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
  /** Initial data - typically data that was preloaded during SSR.*/
  init?: PagedResponseOf<P>;

  /** By default, the first page of data will be loaded when usePagination is initialized.
   * Set `load: false` to prevent data loading until you are ready for it - updating
   * the value to true will trigger loading. */
  load?: boolean;

  /** Query parameters passed to the data source when loading new data.
   * Changing this value will clear the existing data and trigger a fresh reload. */
  query?: Query<P> | undefined;
}

export type PaginationLoader<P extends PathWithPagination> = (
  ...params: Parameters<typeof getPaginated<P>>
) => ReturnType<typeof getPaginated<P>>;

interface PagedDataState<T> {
  items: T[];
  href: AdjacentPages;
  available: number;
}

const initialState = <P extends PathWithPagination>(
  initialData?: PagedResponseOf<P>,
): PagedDataState<PageItemType<P>> => ({
  items: initialData?.items ?? [],
  available: initialData?.count ?? -1,
  href: {
    previous: initialData?.previous ?? null,
    next: initialData?.next ?? null,
  },
});

type PreviousParams<P extends PathWithPagination> = Pick<
  PaginationConfig<P>,
  "load" | "query"
> & { path: P };

export const usePagination = <P extends PathWithPagination>(
  path: P,
  config?: PaginationConfig<P>,
  loader: PaginationLoader<P> = getPaginated,
): Paginated<PageItemType<P>> => {
  type T = PageItemType<P>;

  const isInitialized = useRef(false);

  // Remember inputs so we can detect granular changes and respond accordingly.
  const previousParams = useRef<PreviousParams<P>>({
    path,
    load: config?.load,
    query: config?.query,
  });
  const [stateRef, state, setState] = useRefState<PagedDataState<T>>(
    initialState(config?.init),
  );
  const abortController = useRef<AbortController>(null);
  const [isLoadingRef, isLoading, setIsLoading] = useRefState(false);
  const [errorRef, error, setError] = useRefState<any>(null);

  const reset = useCallback(async (reason?: string) => {
    abortController.current?.abort(reason);
    abortController.current = null;
    setState(initialState());
    setError(null);
    setIsLoading(false);
  }, []);

  const loadNext = useCallback(async () => {
    if (config?.load === false) return;
    if (isLoadingRef.current) return;
    if (errorRef.current) return;
    if (stateRef.current.available >= 0 && !stateRef.current.href.next) return;

    setIsLoading(true);
    abortController.current = new AbortController();

    try {
      const {
        data,
        error: err,
        response,
      } = await loader(
        path,
        {
          query: {
            ...((config?.query ?? {}) as Query<P>),
            offset: stateRef.current.href.next ?? 0,
          },
        },
        abortController?.current?.signal,
      );

      if (err || !data) {
        setError(`${response.status}: ${response.url}`);
        return;
      }

      setState({
        items: [...stateRef.current.items, ...data.items],
        available: data.count,
        href: {
          previous: data.previous,
          next: data.next,
        },
      });
    } catch (e) {
      console.debug(`ERROR ${e}`);
      setError(e);
    } finally {
      setIsLoading(false);
    }
  }, [path, config?.query, config?.load]);

  useEffect(() => {
    if (!isInitialized.current) {
      isInitialized.current = true;

      if (!config?.init) {
        // Load the first page of data if initial (preloaded) data is not provided.
        void loadNext();
      }
      return;
    }

    const previous = previousParams.current;
    if (path !== previous.path || config?.query !== previous.query) {
      void reset().then(loadNext);
    } else if (config?.load && config?.load !== previous.load) {
      void loadNext();
    }
    previousParams.current = {
      path,
      query: config?.query,
      load: config?.load,
    };
  }, [loadNext]);

  return useMemo(() => {
    const hasMore = state.available < 0 || state.available > state.items.length;
    return {
      items: state.items,
      availableItems: state.available,
      href: state.href,
      isLoading,
      error,
      reset,
      hasMore,
      loadNext: hasMore ? loadNext : undefined,
    };
  }, [state, isLoading, error, loadNext]);
};

type RefState<T> = [RefObject<T>, T, (value: T) => void];
const useRefState = <T>(initialValue: T): RefState<T> => {
  const [state, setState] = useState<T>(initialValue);
  const ref = useRef<T>(initialValue);

  const update = useCallback((value: T) => {
    ref.current = value;
    setState(value);
  }, []);

  return [ref, state, update];
};
