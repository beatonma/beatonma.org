import { ReactNode } from "react";
import { Nullish } from "@/types";
import { onlyIf } from "@/util/optional";

interface OptionalProps<T> {
  value: T | Nullish;
  also?: boolean;
  block: (value: T) => ReactNode;
}

export const Optional = <T,>(props: OptionalProps<T>) => {
  const { value, also, block } = props;

  if (also === false) return null;

  return onlyIf(value, block);
};
