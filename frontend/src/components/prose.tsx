import { JSX } from "react";
import CustomElement, { CustomElementProps } from "@/components/element";
import { addClass } from "@/util/transforms";

export default function Prose<T extends keyof JSX.IntrinsicElements>(
  props: CustomElementProps<T>,
) {
  const { ...rest } = addClass(
    props,
    "prose light:prose prose-invert lg:prose-lg light:lg:prose-lg readable! px-edge",
  );
  return <CustomElement {...rest} />;
}
