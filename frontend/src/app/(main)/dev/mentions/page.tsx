import { Metadata } from "next";
import { SampleWebmentions } from "@/app/(main)/dev/_sample";
import { Webmentions } from "@/features/webmentions";

export const metadata: Metadata = {
  title: "Webmentions",
  description: "",
};

export default async function Page() {
  return <Webmentions mentions={SampleWebmentions} />;
}
