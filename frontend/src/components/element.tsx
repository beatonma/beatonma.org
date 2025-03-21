import React, { ComponentPropsWithoutRef, JSX } from "react";

export type ElementName = keyof JSX.IntrinsicElements;
export type CustomElementProps<T extends ElementName> = {
  elementName: T;
} & ComponentPropsWithoutRef<T>;

export default function CustomElement<T extends ElementName>(
  props: CustomElementProps<T>,
) {
  const { elementName, ...rest } = props;

  return React.createElement(elementName, rest);
}
