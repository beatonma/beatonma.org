import {
  ComponentPropsWithRef,
  ComponentPropsWithoutRef,
  Dispatch,
  ElementType,
  ReactNode,
  SetStateAction,
} from "react";
import { MaybeString } from "./index";

export interface ClassNameProps {
  className?: MaybeString;
}

export interface ChildrenProps {
  children?: ReactNode;
}

/* Create a new type based on ElementType with additional or overriding attributes from Extra.
 * In case of a shared attribute, the signature from Extra will be used instead of that from ElementType */
export type Props<
  Element extends ElementType = "div",
  Extra extends object = object,
> = Extra & Omit<ComponentPropsWithoutRef<Element>, keyof Extra>;

/* Create a new type based on ElementType with additional or overriding attributes from Extra.
 * In case of a shared attribute, the signature from Extra will be used instead of that from ElementType */
export type PropsWithRef<
  Element extends ElementType = "div",
  Extra extends object = object,
> = Extra & Omit<ComponentPropsWithRef<Element>, keyof Extra>;

export type DivProps<Extra extends object = object> = Props<"div", Extra>;
export type DivPropsNoChildren<Extra extends object = object> = Omit<
  Props<"div", Extra>,
  "children"
>;

export type PropsExcept<
  Element extends ElementType,
  Except extends keyof ComponentPropsWithoutRef<Element>,
> = Omit<Props<Element>, Except>;

export type StateSetter<S> = Dispatch<SetStateAction<S>>;
