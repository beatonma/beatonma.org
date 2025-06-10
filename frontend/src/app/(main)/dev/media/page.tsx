import { Metadata } from "next";
import {
  SampleMedia,
  SampleMediaMixed,
  SamplePostsWithMedia,
} from "@/app/(main)/dev/_sample";
import { MediaCarousel } from "@/features/media";
import { PostPreview } from "@/features/posts";

export const metadata: Metadata = {
  title: "Media components",
  description: "",
};

export default async function Page() {
  return (
    <div className="readable space-y-8">
      <MediaCarousel
        media={[...SampleMedia, ...SampleMediaMixed]}
        className="max-h-[40vh]"
      />

      <div className="max-w-[60ch] space-y-8 mx-auto">
        {SamplePostsWithMedia.map((post, index) => (
          <PostPreview post={post} key={index} />
        ))}
      </div>
    </div>
  );
}
