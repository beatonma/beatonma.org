"use client";

import {
  FocusEvent,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { SearchablePath } from "@/api";
import { Button } from "@/components/button";
import { PostType } from "@/components/data/posts";
import { PostPreview } from "@/components/data/types";
import { Date } from "@/components/datetime";
import { ScrimBackground } from "@/components/dialog/scrim";
import { useClient } from "@/components/hooks/environment";
import DangerousHtml from "@/components/html";
import { Row } from "@/components/layout";
import Loading from "@/components/loading";
import { MediaThumbnail } from "@/components/media/media-view";
import Optional from "@/components/optional";
import usePagination from "@/components/paginated";
import itemTheme from "@/components/themed/item-theme";
import { navigationHref } from "@/navigation";
import {
  DivPropsNoChildren,
  Props,
  PropsWithRef,
  StateSetter,
} from "@/types/react";
import { testId } from "@/util";
import { onlyIf } from "@/util/optional";
import { addClass, classes } from "@/util/transforms";

const TestTarget = {
  SearchButton: "search_button",
  SearchInput: "search_input",
};
const MinQueryLength = 3;

interface SearchProps<P extends SearchablePath> {
  path: P;
  containerClassName?: string;
  defaultQuery?: string;
}
type SearchDivProps<P extends SearchablePath> = SearchProps<P> &
  Omit<DivPropsNoChildren, keyof SearchProps<P>>;

export default function Search<P extends SearchablePath>(
  props: SearchDivProps<P>,
) {
  const isClient = useClient();

  return isClient ? (
    <ControlledSearch {...props} />
  ) : (
    <NoscriptSearch {...props} />
  );
}

const NoscriptSearch = <P extends SearchablePath>(props: SearchDivProps<P>) => {
  return (
    <noscript className={props.containerClassName}>
      <SearchForm className={props.className} />
    </noscript>
  );
};

const ControlledSearch = <P extends SearchablePath>(
  props: SearchDivProps<P>,
) => {
  const { path, defaultQuery, ...rest } = props;
  const [isActive, setIsActive] = useState(false);
  const [query, setQuery] = useState(defaultQuery ?? "");
  const paginationConfig = useMemo(
    () => ({
      load: isActive && isQueryValid(query),
      query: { query: query },
    }),
    [isActive, query],
  );

  const results = usePagination(path, paginationConfig);

  return (
    <SearchUI
      isActive={isActive}
      setIsActive={setIsActive}
      query={query}
      setQuery={setQuery}
      isLoading={results.isLoading}
      items={results.items as PostPreview[]}
      {...rest}
    />
  );
};

interface SearchUiProps extends SearchBarProps {
  isLoading: boolean;
  items: PostPreview[];
  containerClassName?: string;
}
const SearchUI = (
  props: SearchUiProps & Omit<DivPropsNoChildren, keyof SearchUiProps>,
) => {
  const {
    query,
    setQuery,
    isActive,
    setIsActive,
    isLoading,
    items,
    containerClassName,
    ...rest
  } = props;
  const queryIsValid = isQueryValid(query);

  const onBlur = useCallback((ev: FocusEvent) => {
    if (ev.currentTarget.contains(ev.relatedTarget)) {
      // Focus moved to element within search UI
      return;
    }

    if (ev.currentTarget.contains(document.activeElement)) {
      return;
    }

    setIsActive(false);
  }, []);

  return (
    <ScrimBackground
      isVisible={isActive}
      onClose={() => setIsActive(false)}
      className={containerClassName}
    >
      <div
        {...addClass(rest, "relative [--search-padding:--spacing(4)] w-full")}
        onBlur={onBlur}
      >
        <SearchBar
          query={query}
          setQuery={setQuery}
          isActive={isActive}
          setIsActive={setIsActive}
          className={classes(
            "w-full before:transition-colors before:-inset-(--search-padding) extra-background",
            isActive
              ? "before:surface-input"
              : "bg-transparent max-sm:border-b-vibrant max-sm:border-b-1",
            onlyIf(queryIsValid, "before:rounded-b-none"),
          )}
        />

        <Optional
          value={isActive}
          block={() => (
            <div
              className={classes(
                "absolute rounded-b-md overflow-y-auto surface-alt",
                "max-h-[50vh] space-y-8",
                "-inset-x-(--search-padding) mt-(--search-padding)",
                onlyIf(queryIsValid, "py-4"),
              )}
            >
              <Results
                items={items}
                isLoading={isLoading}
                isQueryValid={queryIsValid}
                itemClassName="col-span-full px-4 py-2"
              />
            </div>
          )}
        />
      </div>
    </ScrimBackground>
  );
};

interface SearchBarProps {
  query: string;
  setQuery: (q: string) => void;
  isActive: boolean;
  setIsActive: StateSetter<boolean>;
}
const SearchBar = (props: SearchBarProps & DivPropsNoChildren) => {
  const { isActive, setIsActive, query, setQuery, ...rest } = props;
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isActive) {
      inputRef.current?.focus();
    }
  }, [isActive]);

  return (
    <Row {...addClass(rest, "w-fit")}>
      <Button
        icon="Search"
        tabIndex={-1}
        onClick={() => setIsActive((prev) => !prev)}
        {...testId(TestTarget.SearchButton)}
      />
      <SearchForm
        ref={inputRef}
        value={query}
        onChange={(ev) => setQuery(ev.target.value)}
        onFocus={() => setIsActive(true)}
        className={classes(
          "outline-0 border-0 ring-0 bg-transparent",
          isActive ? "w-full" : "sm:max-w-0 sm:p-0",
        )}
      />
    </Row>
  );
};
const SearchForm = (props: PropsWithRef<"input">) => {
  return (
    <form action={navigationHref("posts")} method="get" className="w-full">
      <input
        name="query"
        type="search"
        placeholder={`Search ${process.env.NEXT_PUBLIC_SITE_NAME}`}
        {...addClass(props, "w-full")}
        {...testId(TestTarget.SearchInput)}
      />
    </form>
  );
};

const Results = (props: {
  itemClassName: string;
  isLoading: boolean;
  items: PostPreview[];
  isQueryValid: boolean;
}) => {
  const { items, itemClassName, isLoading, isQueryValid } = props;

  if (isLoading) return <Loading className={itemClassName} />;
  if (isQueryValid && !items.length) {
    return <div className={itemClassName}>Nothing here!</div>;
  }

  return (
    <>
      {items.map((item) => (
        <Result key={item.url} post={item} className={itemClassName} />
      ))}
    </>
  );
};

const Result = (props: { post: PostPreview } & Props<"a">) => {
  const { post, style, ...rest } = props;

  return (
    <a
      href={post.url}
      style={itemTheme(post, style)}
      {...addClass(
        rest,
        "grid grid-cols-[1fr_auto] hover-surface-alt hover:no-underline",
      )}
    >
      <div className="col-start-1 space-y-1 overflow-x-hidden">
        <TextContent post={post} />
        <Date className="text-sm text-current/60" date={post.published_at} />
      </div>

      <Optional
        value={post.hero_image ?? post.files?.[0]}
        block={(media) => (
          <MediaThumbnail
            media={media}
            className="w-16 h-16 aspect-square ms-4 rounded-md"
          />
        )}
      />
    </a>
  );
};

const TextContent = (props: { post: PostPreview }) => {
  const { post } = props;

  if (!post.title && !post.content_html) return "(no text)";

  const title = onlyIf(post.title, (title) => (
    <Row className="gap-x-2">
      <strong className="line-clamp-1">{title}</strong>
      <PostType post={post} className="col-start-1 place-self-end" />
    </Row>
  ));
  const previewContent = (
    <DangerousHtml
      className="line-clamp-2"
      html={post.content_html?.replace(/<.*?>/g, "")}
    />
  );

  return (
    <>
      {title}
      {previewContent}
    </>
  );
};

const isQueryValid = (query: string) => query.trim().length >= MinQueryLength;

export const _private = {
  SearchUI,
};
