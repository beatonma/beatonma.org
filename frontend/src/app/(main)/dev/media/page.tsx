import { Metadata } from "next";
import { SampleMedia, SamplePostsWithMedia } from "@/app/(main)/dev/_sample";
import { MediaCarousel } from "@/features/media";
import { PostPreview } from "@/features/posts/many/post-preview";

export const metadata: Metadata = {
  title: "Media components",
  description: "",
};

export default async function Page() {
  return (
    <div className="readable space-y-8">
      <MediaCarousel
        media={SampleMedia}
        className="max-h-[40vh] overflow-hidden"
      />

      <div className="max-w-[60ch] space-y-8">
        {SamplePostsWithMedia.map((post) => (
          <PostPreview post={post} key={post.files.length} />
        ))}
      </div>
    </div>
  );
}
