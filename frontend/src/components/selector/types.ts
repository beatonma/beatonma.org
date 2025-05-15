import { ReactNode } from "react";
import { DivPropsNoChildren } from "@/types/react";

export interface SelectorItem {
  display: ReactNode;
  key: string;
  href: string;
}

export interface SelectorProps {
  selected: SelectorItem;
  items: SelectorItem[];
  onSelect: (selected: SelectorItem) => void;
}

export type SelectorDivProps = SelectorProps &
  Omit<DivPropsNoChildren, keyof SelectorProps>;
