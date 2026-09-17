import { Search } from "@/features/posts/search";
import { Props } from "@/types/react";

export const GlobalSearch = (props: Props<typeof Search>) => (
  <Search {...props} />
);
