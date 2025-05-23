import Search from "@/components/data/posts/search";
import { Props } from "@/types/react";

export default function GlobalSearch(
  props: Omit<Props<typeof Search>, "path">,
) {
  return <Search path="/api/posts/" {...props} />;
}
