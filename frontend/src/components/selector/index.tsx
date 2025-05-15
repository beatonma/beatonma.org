import { NoscriptSelectWrapper } from "@/components/selector/noscript";
import { SelectorDivProps } from "@/components/selector/types";
import { Select as SelectComponent } from "./select";
import { TabBar as TabBarComponent } from "./tabs";

export const Select = (props: SelectorDivProps) => (
  <NoscriptSelectWrapper
    {...props}
    reactNode={() => <SelectComponent {...props} />}
  />
);
export const TabBar = (props: SelectorDivProps) => (
  <NoscriptSelectWrapper
    {...props}
    reactNode={() => <TabBarComponent {...props} />}
  />
);
