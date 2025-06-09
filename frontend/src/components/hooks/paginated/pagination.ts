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
import { StateSetter } from "@/types/react";

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

/** Used to track changes in usePagination inputs. */
type PreviousParams<P extends PathWithPagination> = Pick<
  PaginationConfig<P>,
  "load" | "query"
> & { path: P };

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

export const usePagination = <P extends PathWithPagination>(
  path: P,
  config?: PaginationConfig<P>,
  loader: PaginationLoader<P> = getPaginated,
): Paginated<PageItemType<P>> => {
  const isInitialized = useRef(false);

  // Remember inputs so we can detect granular changes and respond accordingly.
  const previousParams = useRef<PreviousParams<P>>({
    path,
    load: config?.load,
    query: config?.query,
  });

  const abortController = useRef<AbortController>(null);

  /** Values tracked with both useRef and useState.
   * Refs so that repeated calls of loadNext do not try to load the same data multiple times
   * States needed to updated UI. */
  const [error, _setError] = useState<any>(null);
  const errorRef = useRef<any>(error);
  const [isLoading, _setIsLoading] = useState<boolean>(false);
  const isLoadingRef = useRef<boolean>(isLoading);

  type State = PagedDataState<PageItemType<P>>;
  const [state, _setState] = useState<State>(initialState(config?.init));
  const stateRef = useRef<State>(state);

  /** Value setters for above values to keep ref and state in sync with each other. */
  const setState = useSyncState(stateRef, _setState);
  const setIsLoading = useSyncState(isLoadingRef, _setIsLoading);
  const setError = useSyncState(errorRef, _setError);

  const updateQueryInBrowser = useUpdateLocationQuery(config?.query ?? {});

  const reset = useCallback(
    async (reason?: string) => {
      abortController.current?.abort(reason);
      abortController.current = null;
      setState(initialState());
      setError(null);
      setIsLoading(false);
    },
    [setState, setError, setIsLoading],
  );

  const loadNext = useCallback(async () => {
    if (config?.load === false) return;
    if (isLoadingRef.current) return;
    if (errorRef.current) return;
    if (stateRef.current.available >= 0 && !stateRef.current.href.next) return;

    setIsLoading(true);
    abortController.current = new AbortController();

    try {
      const query: Query<P> = {
        ...(config?.query ?? {}),
        offset: stateRef.current.href.next ?? 0,
      };
      const {
        data,
        error: err,
        response,
      } = await loader(path, { query }, abortController?.current?.signal);

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
      updateQueryInBrowser(query);
    } catch (e) {
      setError(e);
    } finally {
      setIsLoading(false);
    }
  }, [
    path,
    config?.query,
    config?.load,
    loader,
    setError,
    setIsLoading,
    setState,
  ]);

  useEffect(() => {
    /* Load first set of data on load, if config allows. */
    if (isInitialized.current) return;

    isInitialized.current = true;
    if (config?.load !== false && !config?.init) {
      // Load the first page of data if initial (preloaded) data is not provided.
      void loadNext();
    }
  }, [loadNext, config?.load, config?.init]);

  useEffect(() => {
    /* After initialization, trigger data loading when parameters change. */
    if (!isInitialized.current) return;

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
  }, [loadNext, config?.load, config?.query, path, reset]);

  return useMemo(() => {
    const hasMore = state.available < 0 || state.available > state.items.length;
    return {
      items: state.items,
      availableItems: state.available,
      href: state.href,
      loadNext: hasMore ? loadNext : undefined,
      isLoading,
      error,
      reset,
      hasMore,
    };
  }, [state, isLoading, error, loadNext, reset]);
};

/** Returns a setter function which updates the given ref and state with the same value. */
const useSyncState = <T>(ref: RefObject<T>, stateSetter: StateSetter<T>) =>
  useCallback(
    (value: T) => {
      ref.current = value;
      stateSetter(value);
    },
    [ref, stateSetter],
  );

const useUpdateLocationQuery = <P extends PathWithPagination>(
  init: Query<P>,
) => {
  const [query, setQuery] = useState(init);

  useEffect(() => {
    const url = new URL(window.location.href);
    const search = url.searchParams;

    Object.entries(query ?? {}).forEach(([k, v]) => {
      if (v) {
        search.set(k, `${v}`);
      } else {
        search.delete(k);
      }
    });

    window.history.replaceState(null, "", url);
  }, [query]);

  return setQuery;
};
