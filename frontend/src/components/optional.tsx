import { ReactNode } from "react";
import CustomElement, { ElementName } from "@/components/element";
import { Nullish } from "@/types";
import { onlyIf } from "@/util/optional";

interface OptionalProps<T> {
  value: T | Nullish;
  el?: ElementName;
  block?: (value: T) => ReactNode;
}
export default function Optional<T>(props: OptionalProps<T>) {
  const { value, el, block } = props;

  if (el) {
    return onlyIf(value as ReactNode, (children) => (
      <CustomElement elementName={el}>{children}</CustomElement>
    ));
  }
  if (block) {
    return onlyIf(value, block);
  }
  throw new Error("<Optional /> requires one of (el | block) arguments");
}
