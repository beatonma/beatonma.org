import { Metadata } from "next";
import { getSlug } from "@/api";
import type { PathWithSlug } from "@/api/client/types";
import { DetailedPost } from "@/api/types";
import { getPlaintextSummaryFromHtml } from "@/components/opengraph/text";

export type SlugParams = { params: Promise<{ slug: string }> };

export const get = async <P extends PathWithSlug>(
  path: P,
  params: SlugParams,
) => getSlug(path, (await params.params).slug);

export const generatePostMetadata = async (
  post: DetailedPost,
  overrides?: {
    title?: string;
    description?: string;
  },
): Promise<Metadata> => {
  const resolvedDescription =
    overrides?.description || post.subtitle || undefined;
  const resolvedTitle =
    overrides?.title ||
    post.title ||
    (!post.content_html
      ? undefined
      : getPlaintextSummaryFromHtml(post.content_html));

  return {
    title: resolvedTitle,
    description: resolvedDescription,
    openGraph: {
      title: resolvedTitle,
      description: resolvedDescription,
      type: "article",
    },
  };
};
