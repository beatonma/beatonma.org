import { PostPreview } from "@/components/data/types";
import { DivPropsNoChildren } from "@/types/react";

export default function MediaPreview(
  props: { media: PostPreview["files"] } & DivPropsNoChildren,
) {
  const { media, ...rest } = props;
  return (
    <div {...rest}>
      {media?.map((item) => (
        <img
          key={item.url}
          src={item.url}
          alt={item.description ?? undefined}
        />
      ))}
    </div>
  );
}
