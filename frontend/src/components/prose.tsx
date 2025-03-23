import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const ProseClassName =
  "prose light:prose prose-invert lg:prose-lg light:lg:prose-lg readable!";

export default function Prose(props: DivProps) {
  const { ...rest } = addClass(props, ProseClassName);
  return <div {...rest} />;
}
