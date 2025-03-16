import { ComponentPropsWithoutRef, ReactNode } from "react";
import { MaybeString } from "./index";

export type DivProps = ComponentPropsWithoutRef<"div">;
export type DivPropsNoChildren = Omit<DivProps, "children">;

export interface ClassNameProps {
  className?: MaybeString;
}

export interface ChildrenProps {
  children?: ReactNode;
}
