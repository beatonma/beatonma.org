"use client";

import React, { ReactNode, useMemo, useState } from "react";
import {
  GlobalState,
  Paged,
  type PostPreview as PostPreviewType,
} from "@/api/types";
import { InlineButton, TintedButton } from "@/components/button";
import Callout from "@/components/callout";
import { GridSpan } from "@/components/grid";
import { Client } from "@/components/hooks/environment";
import { useOnScrollIntoViewRef } from "@/components/hooks/observer";
import usePagination, { type Paginated } from "@/components/hooks/paginated";
import Icon from "@/components/icon";
import { Row } from "@/components/layout";
import { LoadingSpinner } from "@/components/loading";
import { Select } from "@/components/selector";
import { navigationHref } from "@/navigation";
import { DivPropsNoChildren, Props } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { PaginatedPostsProps } from "./paginated-posts";
import { PostPreview } from "./post-preview";

type Feeds = GlobalState["feeds"];

interface InfinitePostsProps extends PaginatedPostsProps {
  init: Paged<PostPreviewType>;
  feeds?: Feeds;
}

export const InfinitePosts = (props: InfinitePostsProps) => {
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
        <PostPreview key={post.url} post={post} />
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
};

const NoscriptPageControls = (
  props: { paged: Paginated<PostPreviewType> } & Props<"noscript">,
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

  const infiniteScrollingRef = useOnScrollIntoViewRef(1, () =>
    pagination.loadNext?.(),
  );

  let content;
  if (pagination.error) {
    content = (
      <Callout level="warn">
        <div className="font-bold">Loading error</div>
        <p>{pagination.error}</p>
      </Callout>
    );
  } else if (!pagination.hasMore) content = endOfContent;
  else if (pagination.isLoading) content = <LoadingSpinner />;
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
