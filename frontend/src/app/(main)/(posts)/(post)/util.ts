import { Metadata } from "next";
import { DetailedPost } from "@/repository/types";
import { getPlaintextSummaryFromHtml } from "@/util/format/string";

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
