"use client";

import { useState } from "react";
import { SamplePosts } from "@/app/(main)/dev/_sample";
import { _private } from "@/features/posts/search";

export const SampleSearch = () => {
  const [query, setQuery] = useState("test");
  const [isVisible, setIsVisible] = useState(true);

  return (
    <_private.SearchUI
      query={query}
      setQuery={setQuery}
      isActive={isVisible}
      setIsActive={setIsVisible}
      isLoading={false}
      items={SamplePosts}
    />
  );
};
