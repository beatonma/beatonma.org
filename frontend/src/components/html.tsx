import Optional from "@/components/optional";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";

export default function DangerousHtml(
  props: Omit<
    DivPropsNoChildren<{ html: string | Nullish }>,
    "dangerouslySetInnerHTML"
  >,
) {
  const { html, ...rest } = props;

  return (
    <Optional
      value={html}
      block={(__html) => <div dangerouslySetInnerHTML={{ __html }} {...rest} />}
    />
  );
}
