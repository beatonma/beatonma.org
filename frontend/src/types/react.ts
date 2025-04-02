import { ComponentPropsWithoutRef, JSX, ReactNode } from "react";
import { MaybeString } from "./index";

export interface ClassNameProps {
  className?: MaybeString;
}

export interface ChildrenProps {
  children?: ReactNode;
}

export type Props<T extends keyof JSX.IntrinsicElements> =
  ComponentPropsWithoutRef<T>;
export type PropsExcept<
  T extends keyof JSX.IntrinsicElements,
  X extends keyof ComponentPropsWithoutRef<T>,
> = Omit<Props<T>, X>;

export type DivProps = Props<"div">;
export type DivPropsNoChildren = PropsExcept<"div", "children">;
