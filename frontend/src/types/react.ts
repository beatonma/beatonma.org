import {
  ComponentProps,
  ComponentPropsWithRef,
  ComponentPropsWithoutRef,
  Dispatch,
  ElementType,
  JSX,
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

export type Props<T extends ElementType = "div"> = ComponentPropsWithoutRef<T>;
export type PropsWithRef<T extends ElementType = "div"> =
  ComponentPropsWithRef<T>;

export type PropsExcept<
  T extends ElementType,
  X extends keyof ComponentPropsWithoutRef<T>,
> = Omit<Props<T>, X>;

export type DivProps = Props;
export type DivPropsNoChildren = PropsExcept<"div", "children">;

export type StateSetter<S> = Dispatch<SetStateAction<S>>;
