import { Metadata } from "next";
import { SampleMedia } from "@/app/dev/_sample";
import MediaCarousel from "@/components/media/media-carousel";

export const metadata: Metadata = {
  title: "Media components",
  description: "",
};

export default async function Page() {
  return (
    <div className="readable">
      <MediaCarousel
        media={SampleMedia}
        className="max-h-[40vh] overflow-hidden"
      />
    </div>
  );
}
