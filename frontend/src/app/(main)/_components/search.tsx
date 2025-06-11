import { Search } from "@/features/posts/search";
import { Props } from "@/types/react";

export const GlobalSearch = (props: Omit<Props<typeof Search>, "path">) => (
  <Search path="/api/posts/" {...props} />
);
