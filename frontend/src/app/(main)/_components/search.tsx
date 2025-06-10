import Search from "@/features/posts/search";
import { Props } from "@/types/react";

export default function GlobalSearch(
  props: Omit<Props<typeof Search>, "path">,
) {
  return <Search path="/api/posts/" {...props} />;
}
