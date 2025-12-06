"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import type { PathWithPagination, Query } from "@/api/client/types";
import { StateSetter } from "@/types/react";

export const useUpdateLocationQuery = <P extends PathWithPagination>(
  updateBrowserLocation: boolean,
  init: Query<P>,
): StateSetter<Query<P>> => {
  const [query, setQuery] = useState(init);
  const router = useRouter();
  const path = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (!updateBrowserLocation) return;
    const search = new URLSearchParams(searchParams);

    Object.entries(query ?? {}).forEach(([k, v]) => {
      if (v) {
        search.set(k, `${v}`);
      } else {
        search.delete(k);
      }
    });
    router.replace(`${path}?${search}`, { scroll: false });
  }, [router, searchParams, path, query, updateBrowserLocation]);

  return setQuery;
};
