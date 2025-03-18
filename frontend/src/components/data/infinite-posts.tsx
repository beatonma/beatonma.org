"use client";

import React, { ReactNode, useEffect, useRef } from "react";
import { Paged } from "@/api";
import { InlineButton, TintedButton } from "@/components/button";
import { PaginatedPostsProps } from "@/components/data/paginated-posts";
import { Post } from "@/components/data/post";
import { PostPreview } from "@/components/data/types";
import { Client } from "@/components/environment";
import { GridSpan } from "@/components/grid";
import { Row } from "@/components/layout";
import Loading from "@/components/loading";
import usePagination, { Paginated } from "@/components/paginated";
import { navigationHref } from "@/navigation";
import { onlyIf } from "@/util/optional";

interface InfinitePostsProps extends PaginatedPostsProps {
  init: Paged<PostPreview>;
}

/**
 * If scripts are allowed, pages are loaded automatically while scrolling.
 * Otherwise links are shown for manual navigation between pages..
 */
export default function InfinitePosts(props: InfinitePostsProps) {
  const { query, init } = props;

  const paged = usePagination("/api/posts/", init, query);

  return (
    <>
      {paged.items.map((post, index) => (
        <Post key={post.url} post={post} />
      ))}

      <LoadNext
        pagination={paged}
        endOfContent={<div className="text-lg">-</div>}
      >
        <noscript className="w-full">
          <Row className="gap-8 justify-between w-full">
            <Row className="gap-2">
              {onlyIf(paged.href.previous, (prev) => (
                <InlineButton
                  href={navigationHref("posts", { offset: prev })}
                  icon="ChevronLeft"
                >
                  Previous
                </InlineButton>
              ))}
            </Row>
            <Row className="gap-2">
              {onlyIf(paged.href.next, (next) => (
                <InlineButton
                  href={navigationHref("posts", { offset: next })}
                  icon="ChevronRight"
                >
                  Next
                </InlineButton>
              ))}
            </Row>
          </Row>
        </noscript>

        <Client>
          <TintedButton onClick={paged.loadNext} className="my-16">
            Load more
          </TintedButton>
        </Client>
      </LoadNext>
    </>
  );
}

const LoadNext = <T,>(props: {
  pagination: Paginated<T>;
  endOfContent?: ReactNode;
  children?: ReactNode;
}) => {
  const { pagination, endOfContent, children } = props;
  const infiniteScrollingRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const target = infiniteScrollingRef.current;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            void pagination.loadNext?.();
            return;
          }
        }
      },
      { threshold: 1 },
    );

    if (target) {
      observer.observe(target);
    }

    return () => {
      if (target) {
        observer.unobserve(target);
      }
    };
  }, [pagination, infiniteScrollingRef]);

  let content;
  if (!pagination.hasMore) content = endOfContent;
  else if (pagination.isLoading) content = <Loading />;
  else if (pagination.loadNext) content = children;
  else content = null;

  return (
    <GridSpan ref={infiniteScrollingRef} className="mb-32 flex justify-center">
      {content}
    </GridSpan>
  );
};
