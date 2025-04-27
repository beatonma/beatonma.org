import { Metadata } from "next";
import { SampleMedia, SamplePostsWithMedia } from "@/app/(main)/dev/_sample";
import Post from "@/components/data/posts/post";
import MediaCarousel from "@/components/media/media-carousel";

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
          <Post post={post} key={post.files.length} />
        ))}
      </div>
    </div>
  );
}
