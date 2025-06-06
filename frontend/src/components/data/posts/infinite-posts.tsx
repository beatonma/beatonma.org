"use client";

import React, { ReactNode, useEffect, useMemo, useRef, useState } from "react";
import { GlobalState, Paged, PostPreview } from "@/api/types";
import { InlineButton, TintedButton } from "@/components/button";
import Callout from "@/components/callout";
import { GridSpan } from "@/components/grid";
import { Client } from "@/components/hooks/environment";
import Icon from "@/components/icon";
import { Row } from "@/components/layout";
import Loading from "@/components/loading";
import usePagination, { Paginated } from "@/components/paginated";
import { Select } from "@/components/selector";
import { navigationHref } from "@/navigation";
import { DivPropsNoChildren, Props } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { PaginatedPostsProps } from "./paginated-posts";
import Post from "./post";

type Feeds = GlobalState["feeds"];

interface InfinitePostsProps extends PaginatedPostsProps {
  init: Paged<PostPreview>;
  feeds?: Feeds;
}

/**
 * If scripts are allowed, pages are loaded automatically while scrolling.
 * Otherwise links are shown for manual navigation between pages.
 */
export default function InfinitePosts(props: InfinitePostsProps) {
  const { feeds, init, query: defaultFilters } = props;
  const [query, setQuery] = useState(defaultFilters);
  const paged = usePagination("/api/posts/", { init, query });

  return (
    <>
      <FeedSelector
        currentFeed={query?.feed}
        feeds={feeds}
        setFeed={(feed) => setQuery((prev) => ({ ...prev, feed }))}
        className="text-sm mb-2 justify-self-center"
      />

      {paged.items.map((post) => (
        <Post key={post.url} post={post} />
      ))}

      <LoadNext
        pagination={paged}
        endOfContent={
          <div className="text-lg">
            <Icon icon="MB" />
          </div>
        }
      >
        <NoscriptPageControls paged={paged} className="w-full" />

        <Client>
          <TintedButton onClick={paged.loadNext} className="my-16">
            Load more
          </TintedButton>
        </Client>
      </LoadNext>
    </>
  );
}

const NoscriptPageControls = (
  props: { paged: Paginated<PostPreview> } & Props<"noscript">,
) => {
  const { paged, ...rest } = props;
  return (
    <noscript {...rest}>
      <Row className="gap-8 justify-between w-full">
        <Row className="gap-2">
          {onlyIf(props.paged.href.previous, (prev) => (
            <InlineButton
              href={navigationHref("posts", { offset: prev })}
              icon="ChevronLeft"
            >
              Previous
            </InlineButton>
          ))}
        </Row>
        <Row className="gap-2">
          {onlyIf(props.paged.href.next, (next) => (
            <InlineButton
              href={navigationHref("posts", { offset: next })}
              icon="ChevronRight"
              reverseLayout={true}
            >
              Next
            </InlineButton>
          ))}
        </Row>
      </Row>
    </noscript>
  );
};

const LoadNext = <T,>(props: {
  pagination: Paginated<T>;
  endOfContent?: ReactNode;
  children?: ReactNode;
}) => {
  const { pagination, endOfContent, children } = props;
  const infiniteScrollingRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (pagination.error) return;
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
  if (pagination.error) {
    content = (
      <Callout level="warn">
        <div className="font-bold">Loading error</div>
        <p>{pagination.error}</p>
      </Callout>
    );
  } else if (!pagination.hasMore) content = endOfContent;
  else if (pagination.isLoading) content = <Loading />;
  else if (pagination.loadNext) content = children;
  else content = null;

  return (
    <GridSpan ref={infiniteScrollingRef} className="mb-32 flex justify-center">
      {content}
    </GridSpan>
  );
};

const FeedSelector = (
  props: DivPropsNoChildren<{
    feeds: Feeds | undefined;
    currentFeed: string | undefined;
    setFeed: (feedSlug: string) => void;
  }>,
) => {
  const { feeds, currentFeed, setFeed, ...rest } = props;
  const feedOptions = useMemo(
    () =>
      feeds?.map((it) => ({
        display: it.name,
        key: it.slug,
        href: navigationHref("posts", { feed: it.slug }),
      })),
    [feeds],
  );

  if (!feedOptions?.length) return null;

  return (
    <Select
      {...rest}
      selected={
        feedOptions.find((it) => it.key === currentFeed) ?? feedOptions[0]
      }
      items={feedOptions}
      onSelect={(it) => {
        setFeed(it.key);
      }}
    />
  );
};
